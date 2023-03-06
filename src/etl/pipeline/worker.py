from .pipeline import Pipeline
from ..extractors.factory import extractor_factory
from ..transformers.transformers import (standardize_column_names,
                                         drop_index_column,
                                         drop_rows_with_missing_values,
                                         convert_date_columns_to_datetime)

DEFAULT_TRANSFORMATIONS = [standardize_column_names,
                           drop_index_column,
                           drop_rows_with_missing_values,
                           convert_date_columns_to_datetime,
                           ]

def run_pipeline(origin_type,
                 origin_path,
                 transformations=DEFAULT_TRANSFORMATIONS):
    try:
        extractor = extractor_factory(origin_type)
        pipe = Pipeline(extractor=extractor,
                        extraction_origin_path=origin_path,
                        transformations=transformations)
        pipe.run()

    except Exception:
        return
