# Dataset Guide

This guide explains how to structure and prepare datasets for training the motor fault diagnosis models.

## Dataset Structure

Organize your dataset by fault class as follows:

```
dataset/
├── healthy/
│   ├── images/
│   │   ├── healthy_001.jpg
│   │   ├── healthy_002.jpg
│   │   └── ...
│   ├── videos/
│   │   ├── healthy_001.mp4
│   │   ├── healthy_002.mp4
│   │   └── ...
│   └── metadata.csv
├── unbalance/
│   ├── images/
│   ├── videos/
│   └── metadata.csv
├── misalignment/
│   ├── images/
│   ├── videos/
│   └── metadata.csv
├── bearing_fault/
│   ├── images/
│   ├── videos/
│   └── metadata.csv
├── rotor_fault/
│   ├── images/
│   ├── videos/
│   └── metadata.csv
├── stator_fault/
│   ├── images/
│   ├── videos/
│   └── metadata.csv
├── looseness/
│   ├── images/
│   ├── videos/
│   └── metadata.csv
└── coupling_fault/
    ├── images/
    ├── videos/
    └── metadata.csv
```

## Metadata Format

Each `metadata.csv` file should contain the following columns:

```csv
filename,motor_id,motor_type,rpm,load,temperature,severity,experimental_condition,date
healthy_001.jpg,M-001,Induction,1450,75,65,Low,Normal operation,2024-01-15
healthy_002.jpg,M-002,Induction,1480,80,70,Low,Normal operation,2024-01-16
```

### Column Descriptions

- **filename**: Name of the image/video file
- **motor_id**: Unique identifier for the motor
- **motor_type**: Type of motor (e.g., Induction, Synchronous)
- **rpm**: Operating speed in revolutions per minute
- **load**: Load percentage (0-100)
- **temperature**: Operating temperature in Celsius
- **severity**: Severity level (Low, Medium, High)
- **experimental_condition**: Description of test conditions
- **date**: Date of data collection

## Image Requirements

### Format
- Supported formats: JPG, JPEG, PNG, BMP, TIFF
- Recommended: PNG or JPG for lossless compression

### Resolution
- Minimum: 64x64 pixels
- Recommended: 512x512 or higher
- Aspect ratio: Square or 4:3 recommended

### Quality
- Clear vibration patterns visible
- Minimal motion blur
- Good contrast between nodal and antinodal regions
- Uniform lighting

### Content
Images should show:
- Chladni patterns on vibrating plates
- Vibration patterns from experimental setups
- Visual representations of motor vibration
- Pattern variations under different fault conditions

## Video Requirements

### Format
- Supported formats: MP4, AVI, MOV, MKV
- Recommended: MP4 with H.264 codec

### Resolution
- Minimum: 640x480
- Recommended: 1280x720 (720p) or higher

### Frame Rate
- Minimum: 15 fps
- Recommended: 30 fps or higher

### Duration
- Minimum: 2 seconds
- Recommended: 5-10 seconds per video
- Maximum: 60 seconds (to manage file size)

### Quality
- Stable camera (minimal shake)
- Clear vibration patterns
- Good lighting
- Minimal compression artifacts

## Dataset Balance

### Class Balance
Aim for balanced classes to avoid bias:
- Each fault class: ~100-500 samples minimum
- Healthy class: Should represent normal operation adequately

### Data Splitting
Recommended split ratios:
- Training: 70%
- Validation: 15%
- Test: 15%

### Important: Avoid Data Leakage
- All frames from the same video must stay in the same split
- All images from the same motor should ideally stay in the same split
- Use motor_id or recording_id for grouping during splitting

## Data Collection Guidelines

### Experimental Setup
1. **Controlled Environment**
   - Consistent lighting conditions
   - Stable mounting of test equipment
   - Controlled motor operating conditions

2. **Parameter Variation**
   - Vary RPM across operating range
   - Test different load conditions
   - Include different motor types

3. **Fault Simulation**
   - Simulate faults safely and consistently
   - Document fault severity levels
   - Record multiple instances of each fault type

4. **Data Labeling**
   - Label by expert inspection
   - Use vibration analysis equipment for validation
   - Document uncertainty in labels

### Quality Control
- Remove corrupted files
- Exclude blurry or unclear images
- Verify file integrity
- Check for duplicate samples

## Data Augmentation

### Allowed Transformations
For Chladni pattern images, use scientifically justified augmentations:

- **Rotation**: Small rotations (±15°) to account for camera angle
- **Brightness/Contrast**: Minor adjustments to account for lighting variation
- **Noise injection**: Gaussian noise to improve robustness

### Avoid Transformations
Do NOT use transformations that physically distort the pattern:
- No extreme rotations (>30°)
- No flipping (changes physical meaning)
- No extreme scaling
- No elastic deformations

## Sample Size Recommendations

### Minimum Viable Dataset
- Total samples: 500-1000
- Per class: 50-100 samples
- Suitable for: Initial prototyping, baseline models

### Research Dataset
- Total samples: 5000-10000
- Per class: 500-1000 samples
- Suitable for: Published research, reliable models

### Production Dataset
- Total samples: 20000+
- Per class: 2000+ samples
- Suitable for: Production deployment, high accuracy

## Data Validation

### Automated Checks
```python
# Validate dataset structure
def validate_dataset(dataset_path):
    """Validate dataset structure and integrity"""
    checks = {
        'structure': check_directory_structure(dataset_path),
        'file_formats': check_file_formats(dataset_path),
        'image_quality': check_image_quality(dataset_path),
        'metadata': check_metadata_files(dataset_path),
        'balance': check_class_balance(dataset_path)
    }
    return checks
```

### Manual Review
- Visual inspection of samples
- Verify labels match visual patterns
- Check for mislabeled samples
- Identify edge cases

## Ethical Considerations

1. **Data Privacy**
   - Remove any identifying information
   - Sanitize metadata if needed

2. **Documentation**
   - Document data collection methods
   - Record experimental conditions
   - Acknowledge data sources

3. **Reproducibility**
   - Maintain detailed records
   - Use version control for dataset
   - Document preprocessing steps

## Dataset Versioning

Use semantic versioning for datasets:
- `v1.0.0`: Initial release
- `v1.1.0`: Added more samples
- `v2.0.0`: Major reorganization or new classes

## Contact

For questions about dataset preparation, refer to the main README or contact the development team.
