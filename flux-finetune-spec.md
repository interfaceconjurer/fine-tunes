# Spec: Fine-Tune Flux 1 on Replicate for Style Transfer

## Goal

Build a Python script that fine-tunes a Flux 1 model on Replicate to learn a specific illustration/art style from a set of reference images, then generates new images in that style. The project should be structured as a clean GitHub repo.

## Repo Structure

```
flux-style-finetune/
├── flux_style_finetune.py    # Main script
├── requirements.txt          # Python dependencies
├── .gitignore
├── .env.example              # Template showing required env vars (no real values)
└── README.md                 # Setup instructions + usage examples
```

### `.gitignore`

```
# Environment / secrets
.env
REPLICATE_API_TOKEN

# Training artifacts
*_training.json
*.zip

# Generated images
outputs/

# Python
__pycache__/
*.pyc
.venv/
venv/

# OS
.DS_Store
Thumbs.db
```

### `.env.example`

```
REPLICATE_API_TOKEN=r8_your_token_here
```

### `requirements.txt`

```
replicate
```

### `README.md`

Include: what this tool does (one paragraph), prerequisites (Python 3.10+, Replicate account), setup steps (clone, install deps, set token), usage examples for all three commands (train, status, generate), and a note about estimated training cost (~$1.50).

## Reference

- Replicate fine-tuning guide: https://replicate.com/docs/get-started/fine-tune-with-flux
- Replicate Python SDK: `pip install replicate`

---

## Prerequisites (script must handle)

1. **Install dependencies**: `replicate` (pip)
2. **API token**: Read `REPLICATE_API_TOKEN` from environment. If not set, print a clear error with instructions:
   - Go to https://replicate.com/account/api-tokens
   - Generate a token
   - `export REPLICATE_API_TOKEN=r8_...`
3. **Replicate username**: Accept via `--username` CLI arg (required). This is the user's Replicate account username.

---

## Script: `flux_style_finetune.py`

### CLI Interface (use `argparse`)

```
python flux_style_finetune.py <command> [options]

Commands:
  train     Package images and launch fine-tuning
  status    Check training status
  generate  Generate images using the fine-tuned model
```

### Command: `train`

**Args:**
| Arg | Required | Default | Description |
|-----|----------|---------|-------------|
| `--images-dir` | yes | — | Path to local directory containing style reference images (PNG/JPG/WebP) |
| `--model-name` | yes | — | Name for the destination model (e.g. `my-art-style`) |
| `--username` | yes | — | Replicate username |
| `--trigger-word` | no | `MYSTYLE` | Trigger word for the style. Must be a unique non-dictionary word. |
| `--steps` | no | `1000` | Number of training steps |

**Behavior:**

1. **Validate images directory:**
   - Confirm directory exists
   - Find all `.png`, `.jpg`, `.jpeg`, `.webp` files
   - Require minimum 2 images, warn if fewer than 10
   - Print count of images found

2. **Package training data:**
   - Create a `.zip` file from all found images
   - Save to a temp location

3. **Create destination model on Replicate (if it doesn't exist):**
   ```python
   model = replicate.models.create(
       owner=args.username,
       name=args.model_name,
       visibility="private",
       hardware="gpu-a40-large"
   )
   ```
   - If model already exists, skip creation (catch the error gracefully)

4. **Upload zip and start training:**
   ```python
   training = replicate.trainings.create(
       model="ostris/flux-dev-lora-trainer",
       version="e440909d7512c4a9d9f684bcd6f20c1bd18aaacf2b68568e30e4413e90e1c424",
       input={
           "input_images": <uploaded zip file or URL>,
           "trigger_word": args.trigger_word,
           "steps": args.steps,
           "lora_rank": 16,
           "optimizer": "adamw8bit",
           "batch_size": 1,
           "resolution": "512,768,1024",
           "autocaption": True,
           "autocaption_prefix": f"In the style of {args.trigger_word},",
       },
       destination=f"{args.username}/{args.model_name}"
   )
   ```
   - **Important**: Look up the current latest version of `ostris/flux-dev-lora-trainer` on Replicate at build time. The version hash above is an example — fetch the real one via:
     ```python
     trainer = replicate.models.get("ostris/flux-dev-lora-trainer")
     version = trainer.latest_version.id
     ```

5. **Print training ID and estimated cost** (~$1.50 for 1000 steps with ~20 images)

6. **Save training metadata** to a local JSON file (`{model_name}_training.json`) containing: training ID, model destination, trigger word, timestamp.

### Command: `status`

**Args:**
| Arg | Required | Description |
|-----|----------|-------------|
| `--training-id` | no | Replicate training ID. If omitted, read from latest `*_training.json` in current dir. |

**Behavior:**

1. Fetch training status via `replicate.trainings.get(training_id)`
2. Print: status (`starting` / `processing` / `succeeded` / `failed`), elapsed time, logs URL
3. If `succeeded`, print the model version ID and a ready-to-use generate command

### Command: `generate`

**Args:**
| Arg | Required | Default | Description |
|-----|----------|---------|-------------|
| `--prompt` | yes | — | Text prompt. The trigger word will be auto-prepended if not already present. |
| `--model-name` | yes | — | Name of the fine-tuned model |
| `--username` | yes | — | Replicate username |
| `--num-outputs` | no | `1` | Number of images to generate (1-4) |
| `--aspect-ratio` | no | `1:1` | Aspect ratio: `1:1`, `16:9`, `9:16`, `4:3`, `3:4` |
| `--output-dir` | no | `./outputs` | Where to save generated images |
| `--guidance-scale` | no | `3.5` | CFG scale |
| `--num-inference-steps` | no | `28` | Number of inference steps |

**Behavior:**

1. Check prompt contains the trigger word; if not, prepend `"In the style of {trigger_word}, "` (read trigger word from `*_training.json` if available)
2. Run inference:
   ```python
   output = replicate.run(
       f"{args.username}/{args.model_name}",
       input={
           "prompt": prompt,
           "num_outputs": args.num_outputs,
           "aspect_ratio": args.aspect_ratio,
           "guidance_scale": args.guidance_scale,
           "num_inference_steps": args.num_inference_steps,
       }
   )
   ```
3. Save output images to `--output-dir` with timestamped filenames
4. Print file paths of saved images

---

## Error Handling

- All API calls wrapped in try/except with clear error messages
- Rate limit errors: retry with exponential backoff (max 3 retries)
- Training failure: print the failure logs from Replicate
- Missing token: don't just crash — print setup instructions
- Invalid images: skip non-image files in the directory with a warning

## Code Quality

- Type hints on all functions
- Docstrings on public functions
- No classes needed — keep it flat and functional
- Use `pathlib.Path` for file operations
- Print progress with timestamps

---

## Usage Example (for reference, not part of the script)

```bash
# 1. Set up
export REPLICATE_API_TOKEN=r8_abc123...

# 2. Train on your style images
python flux_style_finetune.py train \
  --images-dir ./my_style_images \
  --model-name watercolor-v1 \
  --username jordan \
  --trigger-word WTRCLR \
  --steps 1500

# 3. Check progress
python flux_style_finetune.py status

# 4. Generate
python flux_style_finetune.py generate \
  --prompt "a cat sitting on a windowsill at sunset" \
  --model-name watercolor-v1 \
  --username jordan \
  --num-outputs 4 \
  --aspect-ratio 16:9
```

---

## Important Notes for Implementation

1. **Trainer model version**: Do NOT hardcode the version hash for `ostris/flux-dev-lora-trainer`. Fetch the latest version dynamically via the API.
2. **File upload**: Use `replicate.trainings.create()` with a local file path or upload the zip to a publicly accessible URL first. The Replicate Python SDK supports passing open file handles directly.
3. **lora_type**: Set to `"style"` (not `"subject"`) since this is style fine-tuning.
4. **Trigger word**: Default `MYSTYLE` — must not be a real word to avoid prompt pollution.
5. **Autocaptioning**: Enable it. Flux LoRA trainer supports auto-captioning with a prefix, which is ideal for style transfer since we don't need per-image captions.
