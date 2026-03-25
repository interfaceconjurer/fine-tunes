#!/usr/bin/env python3
"""
Flux Style Fine-Tuning Tool

A CLI tool for fine-tuning Flux 1 models on Replicate for style transfer.
"""

import argparse
import os
import sys
import json
import time
import zipfile
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any, Callable
import replicate


# ============================================================================
# Helper Functions
# ============================================================================

def check_replicate_token() -> str:
    """
    Check for REPLICATE_API_TOKEN in environment.

    Returns:
        The API token string

    Exits:
        If token is not found, prints instructions and exits
    """
    token = os.environ.get("REPLICATE_API_TOKEN")
    if not token:
        print("ERROR: REPLICATE_API_TOKEN environment variable not set")
        print()
        print("To set up your Replicate API token:")
        print("1. Get your token from: https://replicate.com/account/api-tokens")
        print("2. Set the environment variable:")
        print("   export REPLICATE_API_TOKEN=r8_your_token_here")
        print()
        print("Or create a .env file and load it before running this script.")
        sys.exit(1)
    return token


def validate_images_directory(images_dir: Path) -> List[Path]:
    """
    Validate the images directory and return list of valid image paths.

    Args:
        images_dir: Path to directory containing training images

    Returns:
        List of valid image file paths

    Exits:
        If directory doesn't exist or contains fewer than 2 images
    """
    if not images_dir.exists():
        print(f"ERROR: Directory not found: {images_dir}")
        sys.exit(1)

    if not images_dir.is_dir():
        print(f"ERROR: Path is not a directory: {images_dir}")
        sys.exit(1)

    # Find all image files
    valid_extensions = {'.png', '.jpg', '.jpeg', '.webp'}
    image_paths = []

    for ext in valid_extensions:
        image_paths.extend(images_dir.glob(f"*{ext}"))
        image_paths.extend(images_dir.glob(f"*{ext.upper()}"))

    # Sort for consistent ordering
    image_paths = sorted(image_paths)

    if len(image_paths) < 2:
        print(f"ERROR: Found only {len(image_paths)} image(s) in {images_dir}")
        print("At least 2 images are required for training.")
        sys.exit(1)

    if len(image_paths) < 10:
        print(f"WARNING: Only {len(image_paths)} images found. For best results, 10-20 images are recommended.")
        print()

    print(f"Found {len(image_paths)} training images")
    return image_paths


def create_training_zip(image_paths: List[Path], output_path: Path) -> Path:
    """
    Create a zip file from the provided image paths.

    Args:
        image_paths: List of image file paths to include
        output_path: Path where zip file should be created

    Returns:
        Path to the created zip file
    """
    print(f"Creating training archive: {output_path.name}")

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for img_path in image_paths:
            zipf.write(img_path, img_path.name)

    print(f"Archive created: {output_path} ({output_path.stat().st_size / 1024 / 1024:.1f} MB)")
    return output_path


def save_training_metadata(
    model_name: str,
    training_id: str,
    destination: str,
    trigger_word: str,
    username: str
) -> None:
    """
    Save training metadata to a JSON file.

    Args:
        model_name: Name of the model
        training_id: Replicate training ID
        destination: Full destination path (username/model_name)
        trigger_word: Style trigger word
        username: Replicate username
    """
    metadata = {
        "model_name": model_name,
        "training_id": training_id,
        "destination": destination,
        "trigger_word": trigger_word,
        "username": username,
        "created_at": datetime.now().isoformat(),
        "status": "starting"
    }

    filename = f"{model_name}_training.json"
    with open(filename, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"Training metadata saved to: {filename}")


def load_training_metadata(model_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Load training metadata from JSON file.

    Args:
        model_name: Specific model name to load, or None for latest

    Returns:
        Dictionary containing training metadata

    Exits:
        If no training metadata file is found
    """
    if model_name:
        filename = f"{model_name}_training.json"
        if not Path(filename).exists():
            print(f"ERROR: Training metadata not found: {filename}")
            sys.exit(1)
    else:
        # Find the most recent training file
        training_files = list(Path.cwd().glob("*_training.json"))
        if not training_files:
            print("ERROR: No training metadata files found in current directory")
            print("Run with --training-id to specify a training ID directly")
            sys.exit(1)

        # Sort by modification time, most recent first
        training_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        filename = training_files[0].name
        print(f"Using latest training file: {filename}")

    with open(filename, 'r') as f:
        return json.load(f)


def retry_with_backoff(func: Callable, *args, max_retries: int = 3, **kwargs) -> Any:
    """
    Execute a function with exponential backoff on rate limit errors.

    Args:
        func: Function to execute
        *args: Positional arguments to pass to the function
        max_retries: Maximum number of retry attempts (keyword-only)
        **kwargs: Keyword arguments to pass to the function

    Returns:
        Result of the function call

    Raises:
        The last exception if all retries are exhausted
    """
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if "rate limit" in str(e).lower() and attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                print(f"Rate limited. Retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
            else:
                raise


# ============================================================================
# Command: Train
# ============================================================================

def command_train(args: argparse.Namespace) -> None:
    """Execute the train command."""
    # Check API token
    check_replicate_token()

    # Validate inputs
    images_dir = Path(args.images_dir)
    image_paths = validate_images_directory(images_dir)

    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting training setup")
    print(f"Model name: {args.model_name}")
    print(f"Username: {args.username}")
    print(f"Trigger word: {args.trigger_word}")
    print(f"Training steps: {args.steps}")
    print()

    # Create training zip
    zip_path = Path(f"{args.model_name}_training_data.zip")
    create_training_zip(image_paths, zip_path)
    print()

    # Get latest version of flux-dev-lora-trainer
    print("Fetching latest trainer version...")
    try:
        trainer = replicate.models.get("ostris/flux-dev-lora-trainer")
        trainer_version = trainer.latest_version.id
        print(f"Using trainer version: {trainer_version[:12]}...")
    except Exception as e:
        print(f"ERROR: Failed to fetch trainer model: {e}")
        sys.exit(1)

    # Create destination model if it doesn't exist
    destination = f"{args.username}/{args.model_name}"
    print(f"\nChecking/creating destination model: {destination}")

    try:
        retry_with_backoff(
            replicate.models.create,
            owner=args.username,
            name=args.model_name,
            visibility="private",
            hardware="gpu-t4"
        )
        print(f"Created new model: {destination}")
    except replicate.exceptions.ReplicateError as e:
        if "already exists" in str(e).lower():
            print(f"Model already exists: {destination}")
        else:
            print(f"ERROR: Failed to create model: {e}")
            sys.exit(1)

    # Start training
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting training...")
    print("This will take approximately 10-20 minutes depending on the number of images and steps.")
    print()

    try:
        training = retry_with_backoff(
            replicate.trainings.create,
            version="ostris/flux-dev-lora-trainer:" + trainer_version,
            input={
                "input_images": open(zip_path, "rb"),
                "trigger_word": args.trigger_word,
                "steps": args.steps,
                "lora_rank": 16,
                "optimizer": "adamw8bit",
                "batch_size": 1,
                "resolution": "512,768,1024",
                "autocaption": True,
                "autocaption_prefix": f"In the style of {args.trigger_word}, ",
                "lora_type": "style"
            },
            destination=destination
        )

        print(f"✓ Training started successfully!")
        print()
        print(f"Training ID: {training.id}")
        print(f"Destination: {destination}")
        print(f"Status URL: https://replicate.com/p/{training.id}")
        print()
        print(f"Estimated cost: ~$1.50 for {args.steps} steps with {len(image_paths)} images")
        print()
        print("To check status, run:")
        print(f"  python flux_style_finetune.py status --training-id {training.id}")
        print()
        print("Or simply:")
        print(f"  python flux_style_finetune.py status")

        # Save training metadata
        save_training_metadata(
            model_name=args.model_name,
            training_id=training.id,
            destination=destination,
            trigger_word=args.trigger_word,
            username=args.username
        )

    except Exception as e:
        print(f"ERROR: Training failed to start: {e}")
        sys.exit(1)


# ============================================================================
# Command: Status
# ============================================================================

def command_status(args: argparse.Namespace) -> None:
    """Execute the status command."""
    check_replicate_token()

    # Get training ID
    if args.training_id:
        training_id = args.training_id
        print(f"Checking status for training: {training_id}")
    else:
        metadata = load_training_metadata()
        training_id = metadata["training_id"]
        print(f"Checking status for model: {metadata['model_name']}")

    print()

    # Fetch training status
    try:
        training = retry_with_backoff(replicate.trainings.get, training_id)

        print(f"Training ID: {training.id}")
        print(f"Status: {training.status}")

        if training.created_at:
            try:
                # Remove timezone info for comparison with datetime.now()
                if hasattr(training.created_at, 'tzinfo') and training.created_at.tzinfo is not None:
                    created_at = training.created_at.replace(tzinfo=None)
                else:
                    created_at = training.created_at
                elapsed = datetime.now() - created_at
                print(f"Elapsed time: {elapsed.total_seconds() / 60:.1f} minutes")
            except:
                pass  # Skip elapsed time if there's an issue

        print(f"Logs URL: https://replicate.com/p/{training.id}")
        print()

        if training.status == "succeeded":
            print("✓ Training completed successfully!")
            print()
            if training.output and "version" in training.output:
                version_id = training.output["version"]
                print(f"Model version: {version_id}")
                print()

            # Get trigger word from metadata if available
            trigger_word = "MYSTYLE"
            try:
                if not args.training_id:
                    trigger_word = metadata.get("trigger_word", "MYSTYLE")
                    model_name = metadata.get("model_name", "model")
                    username = metadata.get("username", "username")
                else:
                    model_name = "model"
                    username = "username"
            except:
                model_name = "model"
                username = "username"

            print("To generate images with your fine-tuned model, run:")
            print(f'  python flux_style_finetune.py generate \\')
            print(f'    --prompt "In the style of {trigger_word}, a magical forest" \\')
            print(f'    --model-name {model_name} \\')
            print(f'    --username {username}')

        elif training.status == "failed":
            print("✗ Training failed")
            if training.error:
                print(f"Error: {training.error}")
            print()
            print(f"Check logs for details: https://replicate.com/p/{training.id}")

        elif training.status in ["starting", "processing"]:
            print("Training is still in progress. Check back in a few minutes.")
            if training.logs:
                print()
                print("Recent logs:")
                print(training.logs[-500:])  # Last 500 characters

        elif training.status == "canceled":
            print("Training was canceled")

    except Exception as e:
        print(f"ERROR: Failed to fetch training status: {e}")
        sys.exit(1)


# ============================================================================
# Command: Generate
# ============================================================================

def command_generate(args: argparse.Namespace) -> None:
    """Execute the generate command."""
    check_replicate_token()

    # Load trigger word from metadata if available
    trigger_word = None
    try:
        metadata = load_training_metadata(args.model_name)
        trigger_word = metadata.get("trigger_word")
    except:
        pass  # Metadata not found, continue without it

    # Check if prompt contains trigger word
    prompt = args.prompt
    if trigger_word and trigger_word.lower() not in prompt.lower():
        prompt = f"In the style of {trigger_word}, {prompt}"
        print(f"Adding trigger word to prompt: {trigger_word}")
        print()

    model_path = f"{args.username}/{args.model_name}"

    # Get the latest version of the model
    try:
        model = replicate.models.get(model_path)
        if model.latest_version:
            model_version = f"{model_path}:{model.latest_version.id}"
        else:
            model_version = model_path
    except:
        # If we can't fetch the model, try with just the path
        model_version = model_path

    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Generating images")
    print(f"Model: {model_path}")
    print(f"Prompt: {prompt}")
    print(f"Number of outputs: {args.num_outputs}")
    print(f"Aspect ratio: {args.aspect_ratio}")
    print()

    # Run inference
    try:
        output = retry_with_backoff(
            replicate.run,
            model_version,
            input={
                "prompt": prompt,
                "num_outputs": args.num_outputs,
                "aspect_ratio": args.aspect_ratio,
                "output_format": "png",
                "guidance_scale": args.guidance_scale,
                "num_inference_steps": args.num_inference_steps,
                "lora_scale": args.lora_scale
            }
        )

        # Create output directory
        output_dir = Path(args.output_dir)
        output_dir.mkdir(exist_ok=True)

        # Download and save images
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_paths = []

        print("Downloading images...")
        for i, image_file in enumerate(output):
            filename = f"{args.model_name}_{timestamp}_{i+1}.png"
            filepath = output_dir / filename

            # Download image (convert FileOutput to string URL)
            import urllib.request
            image_url = str(image_file)
            urllib.request.urlretrieve(image_url, filepath)
            saved_paths.append(filepath)
            print(f"  ✓ Saved: {filepath}")

        print()
        print(f"✓ Generated {len(saved_paths)} image(s)")
        print(f"Saved to: {output_dir}")

    except replicate.exceptions.ModelError as e:
        print(f"ERROR: Model not found or not ready: {model_path}")
        print(f"Please check that:")
        print(f"  - Username is correct: {args.username}")
        print(f"  - Model name is correct: {args.model_name}")
        print(f"  - Training has completed successfully")
        print()
        print(f"Details: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Generation failed: {e}")
        sys.exit(1)


# ============================================================================
# Main CLI
# ============================================================================

def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Flux Style Fine-Tuning Tool - Train and use custom Flux models on Replicate",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Train command
    train_parser = subparsers.add_parser(
        "train",
        help="Start a new style fine-tuning training"
    )
    train_parser.add_argument(
        "--images-dir",
        required=True,
        help="Directory containing training images (PNG, JPG, JPEG, WebP)"
    )
    train_parser.add_argument(
        "--model-name",
        required=True,
        help="Name for your fine-tuned model"
    )
    train_parser.add_argument(
        "--username",
        required=True,
        help="Your Replicate username"
    )
    train_parser.add_argument(
        "--trigger-word",
        default="MYSTYLE",
        help="Trigger word for the style (default: MYSTYLE)"
    )
    train_parser.add_argument(
        "--steps",
        type=int,
        default=1000,
        help="Number of training steps (default: 1000)"
    )

    # Status command
    status_parser = subparsers.add_parser(
        "status",
        help="Check training status"
    )
    status_parser.add_argument(
        "--training-id",
        help="Training ID to check (uses latest if not specified)"
    )

    # Generate command
    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate images with a fine-tuned model"
    )
    generate_parser.add_argument(
        "--prompt",
        required=True,
        help="Text prompt for image generation"
    )
    generate_parser.add_argument(
        "--model-name",
        required=True,
        help="Name of your fine-tuned model"
    )
    generate_parser.add_argument(
        "--username",
        required=True,
        help="Your Replicate username"
    )
    generate_parser.add_argument(
        "--num-outputs",
        type=int,
        default=1,
        choices=[1, 2, 3, 4],
        help="Number of images to generate (1-4, default: 1)"
    )
    generate_parser.add_argument(
        "--aspect-ratio",
        default="1:1",
        choices=["1:1", "16:9", "9:16", "4:3", "3:4"],
        help="Image aspect ratio (default: 1:1)"
    )
    generate_parser.add_argument(
        "--output-dir",
        default="./outputs",
        help="Directory to save generated images (default: ./outputs)"
    )
    generate_parser.add_argument(
        "--guidance-scale",
        type=float,
        default=3.5,
        help="Guidance scale for generation (default: 3.5)"
    )
    generate_parser.add_argument(
        "--num-inference-steps",
        type=int,
        default=28,
        help="Number of inference steps (default: 28)"
    )
    generate_parser.add_argument(
        "--lora-scale",
        type=float,
        default=1.0,
        help="LoRA strength/scale (default: 1.0, try 1.5-2.5 for stronger style)"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Execute command
    if args.command == "train":
        command_train(args)
    elif args.command == "status":
        command_status(args)
    elif args.command == "generate":
        command_generate(args)


if __name__ == "__main__":
    main()
