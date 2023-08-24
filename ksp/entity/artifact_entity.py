from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    feature_store_file_path : str
    train_file_path : str
    test_file_path : str


@dataclass
class DataTransformationArtifact:
    transform_object_path:str
    transform_train_path:str
    transform_test_path:str


@dataclass
class ModelTrainerArtifact:
    model_path : str
    training_accuracy : float
    testing_accuracy : float