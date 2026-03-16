"""
Medical Coding API Endpoints
Main endpoints for processing medical reports
"""

from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.models.requests import ProcessTextRequest
from app.models.responses import Medical_Coding_Response
from app.services.medical_coding_pipeline import Medical_Coding_Pipeline
from app.services.llm_as_judge import LLM_as_Judge


router = APIRouter()


@router.post(
    "/process/text",
    response_model=Medical_Coding_Response,
    summary="Process Medical Report Text",
    description="Process medical report text through the coding pipeline"
)
async def process_medical_text(request: ProcessTextRequest) -> Medical_Coding_Response:
    """
    Process medical report text through the multi-agent coding pipeline.
    
    This endpoint:
    1. Extracts medical entities from the text
    2. Assigns ICD-10-CM diagnosis codes
    3. Assigns CPT-4 procedure codes
    4. Assigns HCPCS Level II codes
    5. Optionally evaluates the coding quality
    
    Args:
        request: ProcessTextRequest with medical report text
        
    Returns:
        PipelineResponse with coding results and optional evaluation
    """
    medical_coding_output = Medical_Coding_Pipeline(request.medical_report_text)
    medical_coding_evaluation = LLM_as_Judge(
        clinical_note=request.medical_report_text,
        medical_coding_output={
            "extracted_entities": medical_coding_output['extracted_entities'],
            "icd_codes": medical_coding_output['icd_codes'],
            "hcpcs_codes": medical_coding_output['hcpcs_codes'],
            "cpt_codes": medical_coding_output['cpt_codes'],
        },
        trace_id=medical_coding_output['trace_id']
    )
    
    # if not medical_coding_evaluation.success:
    #     raise HTTPException(
    #         status_code=500,
    #         detail=f"Pipeline processing failed: {medical_coding_evaluation.error}"
    #     )
    
    if request.include_evaluation:
        medical_coding_output['evaluation'] = medical_coding_evaluation

    return medical_coding_output


# @router.post(
#     "/process-pdf",
#     response_model=PipelineResponse,
#     summary="Process Medical Report PDF",
#     description="Upload and process a medical report PDF through the coding pipeline"
# )
# async def process_medical_pdf(
#     file: UploadFile = File(..., description="PDF file to process"),
#     include_evaluation: bool = True
# ) -> PipelineResponse:
#     """
#     Process uploaded medical report PDF through the multi-agent coding pipeline.
    
#     Args:
#         file: Uploaded PDF file
#         include_evaluation: Whether to include LLM judge evaluation
        
#     Returns:
#         PipelineResponse with coding results and optional evaluation
#     """
#     # Validate file type
#     if not file.filename.lower().endswith('.pdf'):
#         raise HTTPException(
#             status_code=400,
#             detail="Only PDF files are supported"
#         )
    
#     # Read file content
#     try:
#         content = await file.read()
#     except Exception as e:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Failed to read uploaded file: {str(e)}"
#         )
    
#     # Process through pipeline
#     result = coding_pipeline_service.process_pdf_bytes(
#         pdf_bytes=content,
#         include_evaluation=include_evaluation
#     )
    
#     if not result.success:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Pipeline processing failed: {result.error}"
#         )
    
#     return result


# @router.post(
#     "/process-test-pdf",
#     response_model=PipelineResponse,
#     summary="Process Test PDF from Backend",
#     description="Process a test PDF file located in the backend folder (for testing only)"
# )
# async def process_test_pdf(
#     filename: str = "sample_medical_report_1.pdf", 
#     include_evaluation: bool = True
# ) -> PipelineResponse:
#     """
#     Process a test PDF file from the backend folder.
#     This is for TESTING PURPOSES ONLY.
    
#     Args:
#         filename: Name of the PDF file in the backend folder
#         include_evaluation: Whether to include LLM judge evaluation
        
#     Returns:
#         PipelineResponse with coding results and optional evaluation
#     """
#     # Construct path to test file in backend folder
#     backend_dir = Path(__file__).parent.parent.parent.parent.parent
#     pdf_path = backend_dir / filename
    
#     if not pdf_path.exists():
#         raise HTTPException(
#             status_code=404,
#             detail=f"Test PDF file not found: {filename}. "
#                    f"Please place the file in the backend folder: {backend_dir}"
#         )
    
#     # Process through pipeline
#     result = coding_pipeline_service.process_pdf(
#         pdf_path=str(pdf_path),
#         include_evaluation=include_evaluation
#     )
    
#     if not result.success:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Pipeline processing failed: {result.error}"
#         )
    
#     return result
