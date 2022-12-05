from sqlalchemy import *
from sqlalchemy.orm import declarative_base

from fastapi_quickcrud_codegen.db_model import DbModel

Base = declarative_base()
metadata = Base.metadata


class HLTCLAIM20202021GOVT(Base):
    __tablename__ = 'HLT_CLAIM_2020_2021_GOVTs'
    __table_args__ = (
        UniqueConstraint('TXT_INSURER_CODE', 'TXT_TRANSACTION_ID',
                         'LOAD_MONTH', 'RECONCILE_FLAG'),
    )

    id = Column(Integer, primary_key=True,
                server_default=text("nextval('\"HLT_CLAIM_2020_2021_GOVTs_id_seq\"'::regclass)"))
    TXT_TPA_CODE = Column(String(10))
    TXT_INSURER_CODE = Column(String(10))
    TXT_POLICY_NUMBER = Column(String(128))
    TXT_MEMBER_REFERENCE_KEY = Column(String(128))
    EMPLOYEE_ID = Column(String(128))
    DATE_OF_BIRTH = Column(DateTime(True))
    NUM_AGE_OF_INSURED = Column(Integer)
    DATE_POLICY_START = Column(DateTime(True))
    DATE_POLICY_END = Column(DateTime(True))
    TXT_PRODUCT_TYPE = Column(String(128))
    TXT_TYPE_OF_POLICY = Column(String(128))
    BOO_FLOATER_APPLICABLE = Column(String(5))
    TXT_GENDER = Column(String(10))
    NUM_SUM_INSURED = Column(Numeric(30, 2))
    TXT_CLAIM_NUMBER = Column(String(128))
    TXT_DIAGNOSIS_CODE_LEVEL_I = Column(String(128))
    TXT_PROCEDURE_CODE_LEVEL_I = Column(String(1000))
    TXT_NAME_OF_THE_HOSPITAL = Column(String(8000))
    TXT_REGISTRATION_NUMBER_OF_HOSPITAL = Column(String(128))
    TXT_PAN_OF_HOSPITAL = Column(String(128))
    TXT_PIN_CODE_OF_HOSPITAL = Column(String(20))
    DATE_OF_ADMISSION = Column(DateTime(True))
    DATE_OF_DISCHARGE = Column(DateTime(True))
    NUM_TOTAL_AMOUNT_CLAIMED = Column(Numeric(30, 2))
    NUM_ROOM_CHARGES_CLAIMED = Column(Numeric(30, 2))
    NUM_NURSING_CHARGES_CLAIMED = Column(Numeric(30, 2))
    NUM_SURGERY_CHARGES_CLAIMED = Column(Numeric(30, 2))
    NUM_CONSULTATION_CHARGES_CLAIMED = Column(Numeric(30, 2))
    NUM_DIAGONOSTIC_CHARGES_CLAIMED = Column(Numeric(30, 2))
    NUM_MEDICINE_CHARGES_CLAIMED = Column(Numeric(30, 2))
    NUM_MISCELLANEOUS_CHARGES_CLAIMED = Column(Numeric(30, 2))
    NUM_PRE_HOSPITALISATION_EXPENSES_CLAIMED = Column(Numeric(30, 2))
    NUM_POST_HOSPITALISATION_EXPENSES_CLAIMED = Column(Numeric(30, 2))
    NUM_PROFESSIONAL_CHARGES_CLAIMED = Column(Numeric(30, 2))
    NUM_OT_CHARGES_CLAIMED = Column(Numeric(30, 2))
    NUM_SURGICAL_IMPLANT_CHARGES_CLAIMED = Column(Numeric(30, 2))
    NUM_TOTAL_CLAIM_PAID = Column(Numeric(30, 2))
    NUM_INDEMNITY_PAID = Column(Numeric(30, 2))
    NUM_HOSPITAL_DAILY_CASH_BENEFIT_PAID = Column(Numeric(30, 2))
    NUM_CRITICAL_ILLNESS_BENEFIT_PAID = Column(Numeric(30, 2))
    NUM_SURGICAL_CASH_BENEFIT_PAID = Column(Numeric(30, 2))
    NUM_CONVALESCENCE_BENEFIT_PAID = Column(Numeric(30, 2))
    TXT_REASON_FOR_REJECTION_OF_CLAIM = Column(String(128))
    TXT_CLAIM_REMARKS = Column(String(8000))
    TXT_DIAGNOSIS_CODE_LEVEL_II = Column(String(128))
    TXT_DIAGNOSIS_CODE_LEVEL_III = Column(String(128))
    TXT_PROCEDURE_CODE_LEVEL_II = Column(String(128))
    TXT_PROCEDURE_CODE_LEVEL_III = Column(String(128))
    TXT_MEDICAL_HISTORY_LEVEL_I = Column(String(1000))
    TXT_HOSPITAL_CODE = Column(String(128))
    TXT_PROCEDURE_DESCRIPTION_LEVEL_I = Column(String(8000))
    TXT_PROCEDURE_DESCRIPTION_LEVEL_II = Column(String(1000))
    TXT_PROCEDURE_DESCRIPTION_LEVEL_III = Column(String(1000))
    TXT_MEDICAL_HISTORY_LEVEL_II = Column(String(1000))
    TXT_MEDICAL_HISTORY_LEVEL_III = Column(String(8000))
    TXT_REASON_FOR_REDUCTION_OF_CLAIM = Column(String(1000))
    TXT_TYPE_OF_CLAIM_PAYMENT = Column(String(128))
    TXT_SYSTEM_OF_MEDICINE_USED = Column(String(128))
    BOO_HOSPITAL_IS_NETWORK_PROVIDER = Column(String(5))
    NUM_AMOUNT_OF_DEDUCTIBLE = Column(Numeric(30, 2))
    NUM_PERCENTAGE_OF_COPAYMENT = Column(Numeric(20, 3))
    NUM_AMOUNT_OF_COPAYMENT = Column(Numeric(30, 2))
    DATE_OF_PAYMENT = Column(DateTime(True))
    TXT_PAYMENT_REFERENCE_NUMBER = Column(String(128))
    DATE_CLAIM_INTIMATION = Column(DateTime(True))
    NUM_BONUS_SUM_INSURED = Column(Numeric(30, 2))
    BOO_CLAIM_REOPENED_OR_NOT = Column(String(5))
    TXT_CLAIM_STATUS = Column(String(10))
    BOO_SURGICAL_OR_NON_SURGICAL_TREATMENT = Column(String(5))
    BOO_OUT_PATIENT_OR_IN_PATIENT_TREATMENT = Column(String(5))
    TXT_IRDA_PRODUCT_ID = Column(String(128))
    TXT_CRITICAL_ILLNESS_DISEASE_CODE = Column(String(128))
    NUM_OPENING_CLAIM_PROVISION = Column(Numeric(30, 2))
    NUM_CLOSING_CLAIM_PROVISION = Column(Numeric(30, 2))
    TXT_TRANSACTION_ID = Column(String(128))
    DATE_TRANSACTION_ID = Column(DateTime(True))
    TXT_REASON_FOR_HOSPITALISATION = Column(String(128))
    TXT_TREATING_DOCTOR_REGISTRATION_NUMBER = Column(String(128))
    TXT_TYPE_OF_ADMISSION = Column(String(128))
    TXT_ROOM_CATEGORY_OCCUPIED = Column(String(128))
    DATE_OF_RECEIPT_OF_COMPLETE_CLAIM_DOCUMENT = Column(DateTime(True))
    TXT_PATIENT_ID = Column(String(128))
    DATE_OF_COMMENCEMENT_OF_FIRST_INSURANCE_WITHOUT_BREAK = Column(DateTime(True))
    LOAD_MONTH = Column(String(15))
    FILE_NAME = Column(String(1000))
    FINANCIAL_YEAR = Column(String(10))
    RECONCILE_FLAG = Column(String(5), server_default=text("'0'::charactervarying"))
    createdBy = Column(String(128))
    updatedBy = Column(String(128))
    createdAt = Column(DateTime(True))
    updatedAt = Column(DateTime(True))
    dataCategory = Column(String(128), server_default=text("'govt'::character varying"))


from fastapi_quickcrud_codegen import crud_router_builder

model_list = [DbModel(db_model=HLTCLAIM20202021GOVT, prefix="/my_first_api", tags=["sample api"])]
crud_router_builder(
    db_model_list=model_list,
    is_async=True,
    database_url="postgresql+asyncpg://postgres:1234@127.0.0.1:5432/postgres"
)
