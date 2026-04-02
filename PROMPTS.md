# Flux Style Fine-Tuning Prompts

Collection of successful prompts used with the android-dream-v4 model.

## Cityscape Prompts

### Basic Cityscape

```
vast city scape, night life, androids, ambient light, neon highlights
```

### Cityscape with Hologram

```
vast city scape, night life, androids, ambient light, neon highlights, beautiful woman hologram
```

### Cityscape with Clothed Hologram

```
vast city scape, night life, androids, ambient light, neon highlights, beautiful woman hologram wearing elegant dress, clothed
```

### Cityscape with Woman in Armor

```
vast city scape, night life, androids, ambient light, neon highlights, woman hologram wearing full black tactical bodysuit with armor plates, fully covered, dressed, clothed figure
```

_Parameters: --guidance-scale 6.0_

### Cityscape with Non-Hologram Woman

```
vast city scape, night life, androids, ambient light, neon highlights, woman wearing full black tactical bodysuit with armor plates, fully covered, dressed, clothed figure
```

_Parameters: --guidance-scale 6.0_

### Expansive Misty Cityscape

```
misty expansive smoky cityscape, vast urban landscape, night life, sunset, ambient light, neon highlights, woman wearing full black tactical bodysuit with armor plates, towering buildings disappearing into fog, atmospheric perspective, neon lights in distance, dramatic scale
```

### Atmospheric Figure Cityscape

```
misty expansive smoky cityscape, vast urban landscape, towering buildings disappearing into fog, atmospheric perspective, neon lights in distance, dramatic scale, beautiful woman in armored suit
```

---

## Desert Wasteland Prompts

### Desert with Megacity Ruins

```
vast desert wasteland at golden hour, abandoned megacity ruins half-buried in sand, colossal statue emerging from dunes, lone vehicle, warm orange and purple sky, desolate beauty
```

### Desert with Pyramid

```
desert sunset, massive pyramid structure half-buried in sand, lone figure walking toward it, warm golden light, long shadows, dust in air, abandoned technology
```

### Desert Storm

```
desert storm approaching, towering dust clouds, derelict spacecraft half-covered in sand dunes, dramatic red sky, silhouette of explorer, desolate atmosphere
```

### Desert with Android Statue

```
dawn in the desert, ancient android statue emerging from dunes, glowing eyes still active, purple and orange sky, lone vehicle in distance, vast emptiness
```

### Desert Canyon Ruins

```
desert canyon with ruins of megacity carved into cliff walls, sand-covered streets below, warm afternoon light, dramatic scale, woman in tactical suit exploring
```

### Desert Twilight Satellites

```
desert at twilight, constellation of abandoned satellites half-buried in sand, deep purple sky with stars emerging, ethereal mood, peaceful desolation
```

---

## Interior & Enclosed Spaces

### Underground Bar

```
intimate underground bar, warm amber lighting, android bartender, shelves of glowing bottles, holographic menus floating, noir atmosphere, rain-soaked patrons, close perspective
```

### Nature Reclaiming Tech

```
overgrown abandoned building interior, nature reclaiming technology, vines through broken windows, shafts of light, birds nesting in servers, peaceful decay
```

---

## Environmental Variations

### Underwater Ruins

```
underwater scene, submerged abandoned city, shafts of light piercing through murky water, schools of fish swimming through broken windows, coral growing on skyscrapers, serene decay, blue-green tones
```

### Ice Planet

```
ice planet glacier field, frozen megacity locked in ice, aurora borealis dancing overhead, crystalline structures, figure in thermal suit walking across frozen wasteland, ethereal blues and greens, pristine desolation
```

### Night Market

```
bustling market street at night, food vendors with glowing stalls, crowds of people in futuristic clothing, hanging lanterns and neon signs, steam rising from cooking, vibrant colors, life and energy
```

---

## Space & Orbital

### Space Station

```
enormous space station orbiting Earth, industrial architecture, docking bays with ships, solar panels catching sunlight, view of planet below with city lights visible, cosmic scale, deep space backdrop
```

---

## Character Portraits - Male Warriors

### Cybernetic Warrior

```
portrait of weathered male warrior, scarred face, cybernetic eye implant glowing red, black tactical armor with worn plates, rain droplets on face, dramatic side lighting, intense gaze, atmospheric fog background
```

_Parameters: --guidance-scale 5.0_

### Soldier at Sunset

```
portrait of stoic male soldier, shaved head, facial scars, wearing heavy combat armor with helmet under arm, orange sunset lighting from side, weathered expression, atmospheric smoke, battle-worn
```

_Parameters: --guidance-scale 5.0_

### Grizzled Veteran

```
close-up portrait of grizzled warrior, gray beard, cybernetic jaw replacement visible, tactical vest with ammunition, rain on face, blue atmospheric lighting, thousand yard stare, hardened veteran
```

_Parameters: --guidance-scale 5.0_

### Young Fighter Post-Battle

```
portrait of young male fighter, intense eyes, blood on face, black tactical suit torn and damaged, dramatic red backlight, determined expression, post-battle, breathing heavy
```

_Parameters: --guidance-scale 5.0_

### Elite Operative

```
profile portrait of elite operative, sleek black armor with glowing blue tech lines, clean sharp features, professional demeanor, cold blue lighting, futuristic visor pushed up on head, calculating gaze
```

_Parameters: --guidance-scale 5.0_

### Commander

```
portrait of commander, middle-aged, stern face, tactical gear with insignia patches, holographic display reflecting on face, warm amber command center lighting, authority and wisdom, strategic mind
```

_Parameters: --guidance-scale 5.0_

---

## Character Portraits - Female Warriors

### Female Soldier at Sunset

```
portrait of stoic female soldier, shaved head, facial scars, wearing heavy combat armor with helmet under arm, orange sunset lighting from side, weathered expression, atmospheric smoke, battle-worn
```

_Parameters: --guidance-scale 5.0_

### Female Grizzled Veteran

```
close-up portrait of grizzled female warrior, short gray hair, cybernetic jaw replacement visible, tactical vest with ammunition, rain on face, blue atmospheric lighting, thousand yard stare, hardened veteran
```

_Parameters: --guidance-scale 5.0_

### Young Female Fighter

```
portrait of young female fighter, intense eyes, blood on face, black tactical suit torn and damaged, dramatic red backlight, determined expression, post-battle, breathing heavy
```

_Parameters: --guidance-scale 5.0_

### Female Elite Operative

```
profile portrait of elite female operative, sleek black armor with glowing blue tech lines, clean sharp features, professional demeanor, cold blue lighting, futuristic visor pushed up on head, calculating gaze
```

_Parameters: --guidance-scale 5.0_

### Female Commander

```
portrait of female commander, middle-aged, stern face, tactical gear with insignia patches, holographic display reflecting on face, warm amber command center lighting, authority and wisdom, strategic mind
```

_Parameters: --guidance-scale 5.0_

---

## Tips for Best Results

### General Guidelines

- **Aspect Ratio**: 16:9 works best for most scenes
- **LoRA Scale**: 1.0-1.2 for balanced results, higher can cause artifacts
- **Guidance Scale**: 5.0-6.0 for better prompt adherence (especially for clothing/specific details)

### Style Keywords

When you need more illustrated/painterly results, add these:

- "illustrated poster art"
- "painterly style"
- "soft edges"
- "atmospheric fog"
- "warm orange and cool blue color palette"

### Clothing Control

To ensure characters are clothed, be very specific:

- Use high guidance scale (6.0)
- Repeat clothing descriptors: "wearing full black tactical bodysuit with armor plates, fully covered, dressed, clothed figure"
- Avoid the word "hologram" if you don't want translucent/nude figures

### What Works Best

- **Desert scenes**: Show painterly style better than cities
- **Character portraits**: Excellent with guidance-scale 5.0
- **Environmental shots**: Wide aspect ratios (16:9) for epic scale
- **Widescreen cityscapes**: Better illustrated quality than square compositions

### What to Avoid

- Very high lora-scale (1.5+) can cause artifacts/corruption
- Generic prompts without style keywords default to photographic
- The model has a strong tendency to add hologram figures from training data

"forlorn ruins, sunset, apocolyptic, wide aspect ratio, atmospheric fog, desolate landscape, dilapidated statue with a strange light Emanating out of it, illustrated poster art, painterly"

"profile portrait of elite female operative, sleek black armor with glowing blue tech lines, clean sharp features, professional demeanor, cold blue lighting, calculating gaze,forlorn ruins, sunset, apocolyptic, wide aspect ratio, atmospheric fog, desolate landscape, illustrated poster art, painterly"
