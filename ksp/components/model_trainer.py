from sklearn.svm import SVC
from ksp.exception import CustomException
from ksp.entity import config_entity, artifact_entity
import sys,os
from sklearn.metrics import accuracy_score
from ksp.logger import logging
from ksp import utils

class ModelTrainer:
    def __init__(self, model_trainer_config:config_entity.ModelTrainerConfig,
                 data_transformation_artifact :artifact_entity.DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise CustomException(e)
        
    def train_model(self,x,y):
        try :
            svc = SVC(C= 0.1,gamma= 0.1, kernel= 'rbf')
            svc.fit(x,y)
            return svc
        except Exception as e:
            raise CustomException(e)
        

    def initiate_model_trainer(self)->artifact_entity.ModelTrainerArtifact:
        try:
            train_arr = utils.load_numpy_array_data(filepath=self.data_transformation_artifact.transform_train_path)
            test_arr = utils.load_numpy_array_data(filepath=self.data_transformation_artifact.transform_test_path) 

            # logging.info(f"{train_arr[:3,:]}")

            x_train , y_train = train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test = test_arr[:,:-1],test_arr[:,-1]

            # logging.info(f"{x_train}")
            # logging.info(f"{x_test}")

            model = self.train_model(x=x_train,y=y_train)

            y_pred_train = model.predict(x_train)
            accuracy_train_score = accuracy_score(y_train,y_pred_train)

            y_pred_test = model.predict(x_test)

            accuracy_test_score = accuracy_score(y_test,y_pred_test)

            logging.info(f" test accuracy is {accuracy_test_score}")

            if accuracy_test_score < self.model_trainer_config.expected_accuracy:
                raise Exception(f"Model is not good as it gave less accuracy form expectation which is {accuracy_test_score} ")

            diff = (accuracy_train_score - accuracy_test_score)

            if diff > self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Model is over fitted with train and test diff : {diff} ")
            
            utils.save_object(filepath=self.model_trainer_config.model_path,obj=model)

            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(
                model_path=self.model_trainer_config.model_path,
                training_accuracy =accuracy_train_score,
                testing_accuracy = accuracy_test_score
                )

            return model_trainer_artifact

        except Exception as e:
            raise CustomException(e, sys)