
"""
Partially taken from MLInspect
"""

class OperatorType(Enum):
    """
    The different operator types in our DAG
    # Eg. https://github.com/stefan-grafberger/mlinspect/blob/master/mlinspect/backends/_sklearn_backend.py
    """
    DATA_SOURCE = "Data Source"
    SELECTION = "Selection"
    PROJECTION = "Projection"
    PROJECTION_MODIFY = "Projection (Modify)" # not sure how this will be different
    TRANSFORMER = "Transformer" 
    CONCATENATION = "Concatenation"
    ESTIMATOR = "Estimator"
    FIT = "Fit Transformers and Estimators"
    JOIN = "Join"
    GROUP_BY_AGG = "Groupby and Aggregate"
    SPLIT_BOUNDARIES = "Data Split"