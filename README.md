# Flux Style Fine-Tuning Tool

A Python CLI tool for fine-tuning Flux 1 models on Replicate to learn and replicate custom artistic styles. Train a model on your artwork or illustration style, then generate new images in that style.

## Overview

This tool simplifies the process of creating custom Flux LoRA models for style transfer. It handles the entire workflow:

- **Training**: Upload your reference images and train a style-specific LoRA model
- **Monitoring**: Check training progress and get notified when complete
- **Generation**: Create new images in your trained style with simple prompts

## Prerequisites

- **Python 3.10+** installed on your system
- **Replicate account** with API access ([sign up here](https://replicate.com))
- **Training images**: 2-20 images in your target style (PNG, JPG, JPEG, or WebP)

## Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/flux-tuning.git
   cd flux-tuning
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Replicate API token**:

   Get your token from [https://replicate.com/account/api-tokens](https://replicate.com/account/api-tokens)

   ```bash
   export REPLICATE_API_TOKEN=r8_your_token_here
   ```

   Or create a `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env and add your token
   ```

## Usage

### Training a Model

Train a new style model using your reference images:

```bash
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
2. Creates a training archive
3. Starts training on Replicate (~10-20 minutes)
4. Saves training metadata locally for easy status checks

**Cost**: Approximately $1.50 for 1000 steps with 20 images.

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
- `--guidance-scale` (optional): How closely to follow the prompt (default: 3.5)
- `--num-inference-steps` (optional): Quality vs speed tradeoff (default: 28)

**Trigger word**: The tool automatically prepends your trigger word (e.g., "In the style of MYART") if not already in the prompt.

## Tips for Best Results

### Training Data

- **Quality over quantity**: 10-20 high-quality images work better than 50 mediocre ones
- **Consistency**: Images should represent a cohesive style
- **Variety**: Include different subjects, compositions, and lighting
- **Resolution**: Higher resolution images (1024px+) train better
- **Clean images**: Avoid watermarks, text, or UI elements

### Trigger Words

- Use **unique, non-dictionary words** (e.g., "ZNDRART", "MYSTL") to avoid conflicts
- Keep it **short and memorable** (one word preferred)
- **Capitalize** to distinguish from normal prompt text

### Training Steps

- **500 steps**: Quick training, lower quality (~$0.75)
- **1000 steps**: Balanced quality/cost (recommended, ~$1.50)
- **2000 steps**: High quality, more overfitting risk (~$3.00)

### Prompting

- Always include your trigger word or let the tool add it automatically
- Be specific about composition, lighting, and subject details
- Experiment with guidance scale (2.5-7.5 range)
- Use negative prompts in complex scenarios

## Project Structure

```
flux-tuning/
├── flux_style_finetune.py    # Main CLI script
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore patterns
├── .env.example               # Environment variable template
├── README.md                  # This file
└── outputs/                   # Generated images (created automatically)
```

## Troubleshooting

### "REPLICATE_API_TOKEN not set"

Make sure you've exported the environment variable:
```bash
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

## Cost Information

Training costs on Replicate (approximate):

| Steps | Images | Duration | Cost |
|-------|--------|----------|------|
| 500   | 10     | ~8 min   | $0.75 |
| 1000  | 10     | ~12 min  | $1.50 |
| 1000  | 20     | ~18 min  | $1.50 |
| 2000  | 20     | ~30 min  | $3.00 |

Generation costs: ~$0.01-0.03 per image depending on resolution and steps.

## Examples

Train a watercolor style model:
```bash
python flux_style_finetune.py train \
  --images-dir ./watercolor_paintings \
  --model-name watercolor-dream \
  --username myusername \
  --trigger-word WCDREAM \
  --steps 1200
```

Generate a landscape in that style:
```bash
python flux_style_finetune.py generate \
  --prompt "a serene mountain lake with pine trees" \
  --model-name watercolor-dream \
  --username myusername \
  --num-outputs 4 \
  --aspect-ratio 16:9
```

## License

MIT License - feel free to use and modify as needed.

## Contributing

Issues and pull requests welcome! This is a community tool designed to make Flux fine-tuning accessible.

## Acknowledgments

- Built on [Replicate](https://replicate.com) infrastructure
- Uses [Ostris Flux LoRA Trainer](https://replicate.com/ostris/flux-dev-lora-trainer)
- Flux models by Black Forest Labs
