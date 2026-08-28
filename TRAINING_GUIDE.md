# Model Training Guide

This guide explains how to train models for the motor fault diagnosis system.

## Prerequisites

1. **Prepared Dataset**: Follow the DATASET_GUIDE.md to prepare your dataset
2. **Installed Dependencies**: Complete the installation in INSTALLATION.md
3. **Computational Resources**: 
   - CPU: Multi-core processor recommended
   - RAM: 8GB minimum, 16GB recommended
   - GPU: Optional but recommended for deep learning models

## Training Pipeline Overview

```
Dataset Preparation → Feature Extraction → Model Selection → Training → Validation → Evaluation → Deployment
```

## Step 1: Dataset Preparation

### Load Dataset

```python
from pathlib import Path
import pandas as pd

def load_dataset(dataset_path):
    """Load dataset from structured directory"""
    dataset_path = Path(dataset_path)
    data = []
    
    for fault_class in dataset_path.iterdir():
        if fault_class.is_dir():
            metadata_file = fault_class / "metadata.csv"
            if metadata_file.exists():
                df = pd.read_csv(metadata_file)
                df['fault_class'] = fault_class.name
                data.append(df)
    
    return pd.concat(data, ignore_index=True)
```

### Split Dataset

```python
from sklearn.model_selection import train_test_split

def split_dataset(df, test_size=0.15, val_size=0.15):
    """Split dataset into train/val/test sets"""
    # First split: train + val vs test
    train_val, test = train_test_split(
        df, 
        test_size=test_size,
        stratify=df['fault_class'],
        random_state=42
    )
    
    # Second split: train vs val
    train, val = train_test_split(
        train_val,
        test_size=val_size/(1-test_size),
        stratify=train_val['fault_class'],
        random_state=42
    )
    
    return train, val, test
```

## Step 2: Feature Extraction

### Extract Features for Training

```python
from backend.preprocessing.image_processing import ImageProcessor
from backend.features.pattern_features import PatternFeatureExtractor
from backend.features.visual_features import VisualFeatureExtractor
import numpy as np

def extract_image_features(image_path):
    """Extract features from a single image"""
    processor = ImageProcessor()
    pattern_extractor = PatternFeatureExtractor()
    visual_extractor = VisualFeatureExtractor()
    
    # Preprocess
    processed = processor.process(image_path)
    
    # Extract features
    pattern_features = pattern_extractor.extract(processed)
    visual_features = visual_extractor.extract(processed)
    
    # Combine
    all_features = {**pattern_features, **visual_features}
    return all_features

def extract_dataset_features(df, image_dir):
    """Extract features for entire dataset"""
    features_list = []
    labels = []
    
    for _, row in df.iterrows():
        image_path = image_dir / row['fault_class'] / 'images' / row['filename']
        features = extract_image_features(str(image_path))
        features_list.append(features)
        labels.append(row['fault_class'])
    
    return features_list, labels
```

## Step 3: Model Selection

### Available Models

#### Baseline Models
- **Random Forest**: Good for tabular features, interpretable
- **Support Vector Machine (SVM)**: Effective for high-dimensional features
- **Decision Tree**: Highly interpretable, good for simple patterns
- **K-Nearest Neighbors**: Simple, non-parametric

#### Deep Learning Models
- **CNN**: For raw image input
- **ResNet/EfficientNet**: Pre-trained models for transfer learning
- **Vision Transformer**: State-of-the-art for image classification
- **CNN-LSTM**: For video/temporal data

### Model Configuration

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

def get_model(model_type, **params):
    """Get model by type with parameters"""
    if model_type == "random_forest":
        return RandomForestClassifier(
            n_estimators=params.get('n_estimators', 100),
            max_depth=params.get('max_depth', 10),
            random_state=42
        )
    elif model_type == "svm":
        return SVC(
            kernel=params.get('kernel', 'rbf'),
            C=params.get('C', 1.0),
            probability=True,
            random_state=42
        )
    # Add more models as needed
```

## Step 4: Training

### Training Script

```python
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

def train_model(X_train, y_train, X_val, y_val, model_type="random_forest"):
    """Train a model"""
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    
    # Get model
    model = get_model(model_type)
    
    # Train
    model.fit(X_train_scaled, y_train)
    
    # Validate
    val_accuracy = model.score(X_val_scaled, y_val)
    val_predictions = model.predict(X_val_scaled)
    
    # Print report
    print("Validation Accuracy:", val_accuracy)
    print(classification_report(y_val, val_predictions))
    
    return model, scaler, val_accuracy
```

### Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV

def tune_hyperparameters(X_train, y_train, model_type="random_forest"):
    """Tune hyperparameters using grid search"""
    if model_type == "random_forest":
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [5, 10, 15, None],
            'min_samples_split': [2, 5, 10]
        }
    elif model_type == "svm":
        param_grid = {
            'C': [0.1, 1, 10],
            'kernel': ['rbf', 'linear'],
            'gamma': ['scale', 'auto']
        }
    
    model = get_model(model_type)
    grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    
    print("Best parameters:", grid_search.best_params_)
    print("Best score:", grid_search.best_score_)
    
    return grid_search.best_estimator_
```

## Step 5: Evaluation

### Comprehensive Evaluation

```python
def evaluate_model(model, scaler, X_test, y_test):
    """Comprehensive model evaluation"""
    X_test_scaled = scaler.transform(X_test)
    
    # Predictions
    predictions = model.predict(X_test_scaled)
    probabilities = model.predict_proba(X_test_scaled)
    
    # Metrics
    accuracy = model.score(X_test_scaled, y_test)
    
    # Classification report
    report = classification_report(y_test, predictions, output_dict=True)
    
    # Confusion matrix
    cm = confusion_matrix(y_test, predictions)
    
    # Per-class metrics
    metrics = {
        'accuracy': accuracy,
        'precision': report['weighted avg']['precision'],
        'recall': report['weighted avg']['recall'],
        'f1_score': report['weighted avg']['f1-score'],
        'confusion_matrix': cm,
        'classification_report': report
    }
    
    return metrics
```

### Visualize Results

```python
def plot_confusion_matrix(cm, classes):
    """Plot confusion matrix"""
    plt.figure(figsize=(10, 8))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.colorbar()
    
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig('confusion_matrix.png')
    plt.close()

def plot_training_history(history):
    """Plot training history for deep learning models"""
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history['accuracy'], label='Train')
    plt.plot(history['val_accuracy'], label='Validation')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history['loss'], label='Train')
    plt.plot(history['val_loss'], label='Validation')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('training_history.png')
    plt.close()
```

## Step 6: Save Model

```python
def save_model(model, scaler, model_dir, model_name):
    """Save trained model and scaler"""
    model_dir = Path(model_dir)
    model_dir.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(model, model_dir / f"{model_name}.pkl")
    joblib.dump(scaler, model_dir / f"{model_name}_scaler.pkl")
    
    print(f"Model saved to {model_dir / model_name}.pkl")
```

## Complete Training Pipeline

```python
def main():
    """Complete training pipeline"""
    # Configuration
    dataset_path = "dataset"
    model_dir = "backend/models/trained"
    model_name = "image_model"
    model_type = "random_forest"
    
    # Load dataset
    print("Loading dataset...")
    df = load_dataset(dataset_path)
    
    # Split dataset
    print("Splitting dataset...")
    train_df, val_df, test_df = split_dataset(df)
    
    # Extract features
    print("Extracting features...")
    X_train, y_train = extract_dataset_features(train_df, dataset_path)
    X_val, y_val = extract_dataset_features(val_df, dataset_path)
    X_test, y_test = extract_dataset_features(test_df, dataset_path)
    
    # Convert to arrays
    X_train = np.array([list(f.values()) for f in X_train])
    X_val = np.array([list(f.values()) for f in X_val])
    X_test = np.array([list(f.values()) for f in X_test])
    
    # Train model
    print("Training model...")
    model, scaler, val_acc = train_model(
        X_train, y_train, X_val, y_val, model_type
    )
    
    # Evaluate
    print("Evaluating model...")
    metrics = evaluate_model(model, scaler, X_test, y_test)
    
    # Save model
    print("Saving model...")
    save_model(model, scaler, model_dir, model_name)
    
    print("Training complete!")
    print(f"Test Accuracy: {metrics['accuracy']:.4f}")
    print(f"F1 Score: {metrics['f1_score']:.4f}")

if __name__ == "__main__":
    main()
```

## Training Tips

### Data Quality
- Ensure balanced classes
- Remove outliers
- Handle missing values
- Verify labels

### Feature Engineering
- Normalize features
- Handle categorical variables
- Feature selection if needed
- Domain knowledge integration

### Model Selection
- Start with simple models
- Progress to complex models
- Consider interpretability
- Match model to data size

### Training Process
- Use cross-validation
- Monitor for overfitting
- Early stopping for deep learning
- Save checkpoints

### Evaluation
- Use multiple metrics
- Confusion matrix analysis
- Per-class performance
- Error analysis

## Common Issues

### Overfitting
- **Symptoms**: High train accuracy, low test accuracy
- **Solutions**: 
  - More training data
  - Regularization
  - Simpler model
  - Data augmentation

### Underfitting
- **Symptoms**: Low accuracy on both train and test
- **Solutions**:
  - More complex model
  - Better features
  - Longer training
  - Hyperparameter tuning

### Class Imbalance
- **Symptoms**: Poor performance on minority classes
- **Solutions**:
  - Balanced sampling
  - Class weights
  - SMOTE augmentation
  - Different evaluation metrics

## Advanced Topics

### Transfer Learning
For deep learning models, use pre-trained weights:

```python
import torchvision.models as models

# Load pre-trained ResNet
model = models.resnet50(pretrained=True)
# Modify final layer for your classes
model.fc = nn.Linear(num_ftrs, num_classes)
```

### Ensemble Methods
Combine multiple models for better performance:

```python
from sklearn.ensemble import VotingClassifier

ensemble = VotingClassifier([
    ('rf', RandomForestClassifier()),
    ('svm', SVC(probability=True)),
    ('knn', KNeighborsClassifier())
], voting='soft')
```

### Cross-Validation
Use k-fold cross-validation for robust evaluation:

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5)
print(f"CV Accuracy: {scores.mean():.4f} (+/- {scores.std():.4f})")
```

## Next Steps

After training:
1. Evaluate on held-out test set
2. Analyze errors and edge cases
3. Deploy model to production
4. Monitor performance in production
5. Collect feedback for retraining

## Support

For training issues, refer to the main README or contact the development team.
