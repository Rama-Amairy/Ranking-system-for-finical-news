from abc import ABC, abstractmethod


class BaseModelHandler(ABC):
    """
    Abstract base class for machine learning models.
    """

    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def load_model(self):
        """Load the specified model."""
        pass

    @abstractmethod
    def predict(self, context: str, question: str):
        """Perform prediction using the model."""
        pass
