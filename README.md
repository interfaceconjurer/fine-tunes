<p align="center">
  <img src="docs/hero-image.png" alt="Flux Style Tuning" width="100%">
</p>

```
  ███████╗██╗     ██╗   ██╗██╗  ██╗    ███████╗████████╗██╗   ██╗██╗     ███████╗
  ██╔════╝██║     ██║   ██║╚██╗██╔╝    ██╔════╝╚══██╔══╝╚██╗ ██╔╝██║     ██╔════╝
  █████╗  ██║     ██║   ██║ ╚███╔╝     ███████╗   ██║    ╚████╔╝ ██║     █████╗
  ██╔══╝  ██║     ██║   ██║ ██╔██╗     ╚════██║   ██║     ╚██╔╝  ██║     ██╔══╝
  ██║     ███████╗╚██████╔╝██╔╝ ██╗    ███████║   ██║      ██║   ███████╗███████╗
  ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝    ╚══════╝   ╚═╝      ╚═╝   ╚══════╝╚══════╝

           ████████╗██╗   ██╗███╗   ██╗██╗███╗   ██╗ ██████╗
           ╚══██╔══╝██║   ██║████╗  ██║██║████╗  ██║██╔════╝
              ██║   ██║   ██║██╔██╗ ██║██║██╔██╗ ██║██║  ███╗
              ██║   ██║   ██║██║╚██╗██║██║██║╚██╗██║██║   ██║
              ██║   ╚██████╔╝██║ ╚████║██║██║ ╚████║╚██████╔╝
              ╚═╝    ╚═════╝ ╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚═════╝
```

[Python 3.10+](https://www.python.org/downloads/)
[License: MIT](https://opensource.org/licenses/MIT)
[Replicate](https://replicate.com)

_Train custom AI art models on your style • Generate infinite variations • Transform any image_

```
╔══════════════════════════════════════════════════════════════════════════════╗
║  A Python CLI tool for fine-tuning Flux 1 models on Replicate to learn and   ║
║  replicate custom artistic styles. Train a model on your artwork, then       ║
║  generate new images in that style with simple prompts.                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## 📋 Table of Contents

- [Overview](#overview)
- [Workflow](#workflow)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Training a Model](#training-a-model)
  - [Checking Training Status](#checking-training-status)
  - [Generating Images](#generating-images)
  - [Image-to-Image Generation](#image-to-image-generation)
- [Advanced Features](#advanced-features)
- [Tips for Best Results](#tips-for-best-results)
- [Prompt Library](#prompt-library)
- [Cost Information](#cost-information)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Project Structure](#project-structure)

## Overview

This tool simplifies the process of creating custom Flux LoRA models for style transfer. It handles the entire workflow:

<p align="center">
  <img src="docs/diagrams/overview-cards.svg" alt="Flux Tuning Overview" width="800">
</p>

<p align="center">
  <img src="docs/diagrams/pipeline.svg" alt="Flux Style Pipeline" width="900">
</p>

<p align="center">
  <img src="docs/diagrams/workflow-linear.svg" alt="Complete Flux Workflow" width="900">
</p>

<p align="center">
  <img src="docs/diagrams/prerequisites.svg" alt="Prerequisites Checklist" width="800">
</p>

## Installation

1. **Clone this repository**:

```bash
# Clone and navigate to the project
git clone https://github.com/yourusername/flux-tuning.git
cd flux-tuning
```

1. **Install dependencies**:

```bash
# Install required Python packages
pip install -r requirements.txt
```

1. **Set up your Replicate API token**:
   Get your token from [https://replicate.com/account/api-tokens](https://replicate.com/account/api-tokens)
   Or create a `.env` file:

&nbsp;
&nbsp;

## Quick Start

<p align="center">
  <img src="docs/diagrams/quick-start.svg" alt="Quick Start Guide" width="900">
</p>

**Step 1️⃣ : Train Your Model**

```bash
# Train a model on your artwork
python flux_style_finetune.py train \
  --images-dir ./my_artwork \
  --model-name my-art-style \
  --username your_replicate_username
```

```
    ⏳ Training starts... (~10-20 minutes)
```

**Step 2️⃣ : Check Status**

```bash
# Monitor training progress
python flux_style_finetune.py status
```

```
    ✅ Training complete! Model ready to use.
```

**Step 3️⃣ : Generate Images**

```bash
# Generate images in your trained style
python flux_style_finetune.py generate \
  --prompt "a magical forest at sunset" \
  --model-name my-art-style \
  --username your_replicate_username
```

```
    🎨 Generated image saved to ./outputs/
```

## Usage

**Quick Commands:**

```bash
# 1. Train your model
python flux_style_finetune.py train --images-dir ./my_artwork --model-name my-style --username you

# 2. Check training status
python flux_style_finetune.py status

# 3. Generate images
python flux_style_finetune.py generate --prompt "your prompt" --model-name my-style --username you

# 3b. Transform existing images (img2img)
python flux_style_finetune.py generate --image ./photo.jpg --prompt "style it" --model-name my-style --username you
```

### Training a Model

Train a new style model using your reference images:

```bash
# Train with custom trigger word and step count
python flux_style_finetune.py train \
  --images-dir ./my_artwork \
  --model-name my-art-style \
  --username your_replicate_username \
  --trigger-word MYART \
  --steps 1000
```

**Parameters**:

- `--images-dir` (required): Directory containing your training images
- `--model-name` (required): Name for your model (lowercase, hyphens allowed)
- `--username` (required): Your Replicate username
- `--trigger-word` (optional): Unique word to activate the style (default: MYSTYLE)
- `--steps` (optional): Training steps, more steps = better quality but higher cost (default: 1000)

**What happens**:

1. Validates your images (minimum 2, recommends 10-20)
2. Bundles images and any matching `.txt` caption files
3. Creates a training archive
4. Starts training on Replicate (~10-20 minutes)
5. Saves training metadata locally for easy status checks

**Cost**: Approximately $1.50 for 1000 steps with 20 images.

#### Custom Captions

To provide custom captions for your training images, create `.txt` files with the same name as your images:

```
my_artwork/
├── image1.jpg
├── image1.txt       # "a dramatic sunset over mountains"
├── image2.png
└── image2.txt       # "a serene forest landscape"
```

The tool will automatically include caption files when creating the training archive.

### Checking Training Status

Check on your training progress:

```bash
# Check latest training
python flux_style_finetune.py status

# Check specific training by ID
python flux_style_finetune.py status --training-id <training_id>
```

Shows:

- Current status (starting/processing/succeeded/failed)
- Elapsed time
- Link to detailed logs
- Instructions for generating images once complete

### Generating Images

Once training is complete, generate images in your style:

```bash
# Generate multiple images in widescreen format
python flux_style_finetune.py generate \
  --prompt "a magical forest at sunset" \
  --model-name my-art-style \
  --username your_replicate_username \
  --num-outputs 2 \
  --aspect-ratio 16:9
```

**Parameters**:

- `--prompt` (required): Text description of what you want to generate
- `--model-name` (required): Name of your trained model
- `--username` (required): Your Replicate username
- `--num-outputs` (optional): Number of images to generate, 1-4 (default: 1)
- `--aspect-ratio` (optional): Image dimensions (default: 1:1)
  - Options: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`
- `--output-dir` (optional): Where to save images (default: ./outputs)
- `--guidance-scale` (optional): How closely to follow the prompt, 1.0-10.0 (default: 3.5)
- `--num-inference-steps` (optional): Quality vs speed tradeoff, 1-50 (default: 28)
- `--lora-scale` (optional): Strength of style application, 0.0-2.0 (default: 1.0)

**Trigger word**: The tool automatically prepends your trigger word (e.g., "In the style of MYART") if not already in the prompt.

### Image-to-Image Generation

Transform existing images using your trained style:

```bash
# Transform an existing image with your style
python flux_style_finetune.py generate \
  --prompt "transform into watercolor painting" \
  --model-name my-art-style \
  --username your_replicate_username \
  --image ./input_photo.jpg \
  --prompt-strength 0.7 \
  --aspect-ratio 16:9
```

**Additional Parameters for img2img**:

- `--image` (required for img2img): Path to input image to transform
- `--prompt-strength` (optional): How much to transform the input, 0.0-1.0 (default: 0.8)
  - `0.0-0.3`: Subtle style transfer, preserves most details
  - `0.4-0.6`: Balanced transformation
  - `0.7-1.0`: Strong transformation, more creative interpretation

**Use cases**:

- Apply your artistic style to photographs
- Iterate on generated images
- Create variations of existing artwork
- Style transfer between different art styles

## Advanced Features

### LoRA Scale Control

Fine-tune how strongly your trained style is applied:

```bash
# Adjust style strength with lora-scale
python flux_style_finetune.py generate \
  --prompt "a serene landscape" \
  --model-name my-art-style \
  --username your_replicate_username \
  --lora-scale 0.8
```

**LoRA Scale Visual Guide**:

### Combining Parameters

Create sophisticated generations by combining parameters:

```bash
# Strong style, subtle transformation of input image
python flux_style_finetune.py generate \
  --prompt "epic mountain vista" \
  --model-name my-art-style \
  --username your_replicate_username \
  --image ./photo.jpg \
  --lora-scale 1.3 \
  --prompt-strength 0.5 \
  --guidance-scale 6.0 \
  --aspect-ratio 16:9 \
  --num-outputs 4
```

## Tips for Best Results

```
╔══════════════════════════════════════════════════════════════════════╗
║              💡 PRO TIPS FOR MAXIMUM QUALITY                         ║
╚══════════════════════════════════════════════════════════════════════╝
```

### 🖼️ Training Data

- **Quality over quantity**: 10-20 high-quality images work better than 50 mediocre ones
- **Consistency**: Images should represent a cohesive style
- **Variety**: Include different subjects, compositions, and lighting
- **Resolution**: Higher resolution images (1024px+) train better
- **Clean images**: Avoid watermarks, text, or UI elements
- **Custom captions**: Use `.txt` files for precise image descriptions

### 🏷️ Trigger Words

- Use **unique, non-dictionary words** (e.g., "ZNDRART", "MYSTL") to avoid conflicts
- Keep it **short and memorable** (one word preferred)
- **Capitalize** to distinguish from normal prompt text

### ⚙️ Training Steps

| Steps | Quality | Cost   | Recommended For                   |
| ----- | ------- | ------ | --------------------------------- |
| 500   | Basic   | ~$0.75 | Quick tests, simple styles        |
| 1000  | Good    | ~$1.50 | **Most use cases** (recommended)  |
| 2000  | High    | ~$3.00 | Complex styles, professional work |

⚠️ **Note**: More steps can lead to overfitting. Start with 1000 and adjust based on results.

### ✍️ Prompting

- Always include your trigger word or let the tool add it automatically
- Be specific about composition, lighting, and subject details
- Experiment with guidance scale (2.5-7.5 range)
- Higher guidance scale (5.0-6.0) helps with specific details like clothing
- Use negative prompts in complex scenarios

### 📊 Parameter Quick Reference

| Parameter             | Range    | Sweet Spot | Effect                                 |
| --------------------- | -------- | ---------- | -------------------------------------- |
| `guidance-scale`      | 1.0-10.0 | 3.5-6.0    | Higher = more prompt adherence         |
| `lora-scale`          | 0.0-2.0  | 1.0-1.2    | Higher = stronger style                |
| `prompt-strength`     | 0.0-1.0  | 0.5-0.7    | (img2img) Higher = more transformation |
| `num-inference-steps` | 1-50     | 28-35      | Higher = better quality, slower        |

## Prompt Library

```
╔══════════════════════════════════════════════════════════════════════╗
║              📚 COMPREHENSIVE PROMPT COLLECTION                      ║
║                                                                      ║
║         30+ Battle-Tested Prompts Ready to Use!                      ║
║         → Check out PROMPTS.md for the full library                  ║
╚══════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────┐
│  🏙️  CITYSCAPE PROMPTS                                                │
│     Neon-lit urban environments • Atmospheric fog • Dramatic scale   │
│                                                                      │
│  🏜️  DESERT WASTELAND PROMPTS                                         │
│     Post-apocalyptic landscapes • Golden hour • Desolate beauty      │
│                                                                      │
│  🏠  INTERIOR & ENCLOSED SPACES                                       │
│     Underground bars • Overgrown buildings • Intimate settings       │
│                                                                      │
│  🌊  ENVIRONMENTAL VARIATIONS                                         │
│     Underwater ruins • Ice planets • Night markets • Unique biomes   │
│                                                                      │
│  🚀  SPACE & ORBITAL                                                  │
│     Space stations • Cosmic backdrops • Orbital views • Sci-fi       │
│                                                                      │
│  🧑‍🚀  CHARACTER PORTRAITS                                              │
│     Warriors • Cybernetic enhancements • Tactical gear • Detailed    │
│                                                                      │
│  💡  TIPS & TECHNIQUES                                                │
│     Style keywords • Clothing control • Parameter recommendations    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**➡️ [View Full Prompt Library (PROMPTS.md)](PROMPTS.md)**

Each prompt includes:

- ✅ Exact prompt text (copy & paste ready)
- ✅ Recommended parameters (guidance-scale, aspect-ratio, etc.)
- ✅ Usage notes from real testing
- ✅ Tips for best results

## Cost Information

```
╔══════════════════════════════════════════════════════════════════════╗
║                       💰 PRICING BREAKDOWN                           ║
╚══════════════════════════════════════════════════════════════════════╝
```

### Training Costs

### Generation Costs

## Examples

```
╔══════════════════════════════════════════════════════════════════════╗
║                     📚 REAL-WORLD EXAMPLES                           ║
╚══════════════════════════════════════════════════════════════════════╝
```

### Example 1: 🎨 Watercolor Style

Train a watercolor style model:

```bash
# Train a watercolor-specific model with 1200 steps
python flux_style_finetune.py train \
  --images-dir ./watercolor_paintings \
  --model-name watercolor-dream \
  --username myusername \
  --trigger-word WCDREAM \
  --steps 1200
```

Generate a landscape in that style:

```bash
# Generate 4 landscape variations
python flux_style_finetune.py generate \
  --prompt "a serene mountain lake with pine trees" \
  --model-name watercolor-dream \
  --username myusername \
  --num-outputs 4 \
  --aspect-ratio 16:9
```

### Example 2: 📸 Photo to Art Transformation

Transform a photograph using your style:

```bash
# Transform a photo with balanced settings
python flux_style_finetune.py generate \
  --prompt "artistic interpretation, dramatic lighting" \
  --model-name watercolor-dream \
  --username myusername \
  --image ./vacation_photo.jpg \
  --prompt-strength 0.6 \
  --lora-scale 1.2 \
  --aspect-ratio 16:9
```

### Example 3: 🧑‍🎨 Character Portrait Generation

Generate a detailed character portrait:

```bash
# Generate a detailed portrait with higher guidance
python flux_style_finetune.py generate \
  --prompt "portrait of a weathered warrior, scarred face, dramatic lighting" \
  --model-name my-art-style \
  --username myusername \
  --guidance-scale 5.0 \
  --aspect-ratio 1:1
```

## Troubleshooting

```
╔══════════════════════════════════════════════════════════════════════╗
║                    🔧 COMMON ISSUES & SOLUTIONS                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

### "REPLICATE_API_TOKEN not set"

Make sure you've exported the environment variable:

```bash
# Set your Replicate API token
export REPLICATE_API_TOKEN=r8_your_actual_token
```

### "Model not found"

Double-check:

- Your username is spelled correctly
- The model name matches what you used during training
- Training completed successfully (run `status` command)

### "Rate limit" errors

The tool automatically retries with exponential backoff. If it persists, wait a minute and try again.

### Training failed

Check the logs URL provided in the output. Common issues:

- Images too small or corrupted
- Insufficient variety in training data
- Not enough disk space

### Poor quality generations

Try adjusting:

- Increase `--guidance-scale` (5.0-6.0) for more prompt adherence
- Adjust `--lora-scale` (0.8-1.2) to control style strength
- Use more specific prompts with detailed descriptions
- Check the [PROMPTS.md](PROMPTS.md) library for proven examples

### Image-to-image not working as expected

- Lower `--prompt-strength` (0.4-0.6) to preserve more of the input image
- Higher `--prompt-strength` (0.7-0.9) for more dramatic transformations
- Ensure input image is high quality (1024px+ recommended)

## Project Structure

```
flux-tuning/
├── flux_style_finetune.py    # Main CLI script
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore patterns
├── .env.example               # Environment variable template
├── README.md                  # This file
├── PROMPTS.md                 # Comprehensive prompt library
└── outputs/                   # Generated images (created automatically)
```

## License

MIT License - feel free to use and modify as needed.

## Contributing

Issues and pull requests welcome! This is a community tool designed to make Flux fine-tuning accessible.

## Acknowledgments

- Built on [Replicate](https://replicate.com) infrastructure
- Uses [Ostris Flux LoRA Trainer](https://replicate.com/ostris/flux-dev-lora-trainer)
- Flux models by Black Forest Labs

```
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                    Happy Creating! 🎨✨                             ║
║                                                                      ║
║         Transform your artistic vision into AI-powered reality       ║
║                                                                      ║
║  Questions? Check PROMPTS.md for inspiration & examples              ║
║  Issues? Open a ticket on GitHub                                     ║
║  Love it? Star the repo and share your creations!                    ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

        Made with ❤️ by the AI art community
        Powered by Replicate • Flux • Black Forest Labs
```
