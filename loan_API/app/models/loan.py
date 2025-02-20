from sqlmodel import SQLModel, Field, Relationship
from uuid import uuid4, UUID
from typing import Optional, List, Dict
from enum import Enum
from sqlalchemy import JSON, Column

import cloudpickle
import pandas as pd
import shap

ex_data = {"State" : "OH",
        "Bank" : "CAPITAL ONE NATL ASSOC",
        "NAICS" : 54,
        "Term" : 60,
        "NoEmp" : 13,
        "NewExist" : 1,
        "CreateJob" : 0,
        "RetainedJob":3,
        "UrbanRural":2,
        "RevLineCr":"N",
        "LowDoc":"N",
        "GrAppv":50000,
        "Recession":0,
        "HasFranchise":1
        }

class StateEnum(str, Enum):
    MN = "MN"
    UT = "UT"
    LA = "LA"
    IN = "IN"
    MA = "MA"
    KY = "KY"
    MT = "MT"
    NY = "NY"
    FL = "FL"
    GA = "GA"
    CO = "CO"
    OH = "OH"
    NH = "NH"
    CA = "CA"
    NC = "NC"
    SC = "SC"
    SD = "SD"
    MD = "MD"
    WA = "WA"
    AZ = "AZ"
    WV = "WV"
    PA = "PA"
    DE = "DE"
    TX = "TX"
    MI = "MI"
    ID = "ID"
    AL = "AL"
    IL = "IL"
    AK = "AK"
    WI = "WI"
    OK = "OK"
    IA = "IA"
    ND = "ND"
    NJ = "NJ"
    RI = "RI"
    MS = "MS"
    MO = "MO"
    CT = "CT"
    NV = "NV"
    OR = "OR"
    ME = "ME"
    VA = "VA"
    KS = "KS"
    AR = "AR"
    NM = "NM"
    TN = "TN"
    NE = "NE"
    VT = "VT"
    HI = "HI"
    WY = "WY"
    DC = "DC"


class NAICSEnum(str, Enum):
    NAICS_32 = "32"
    NAICS_61 = "61"
    NAICS_33 = "33"
    NAICS_56 = "56"
    NAICS_44 = "44"
    NAICS_54 = "54"
    NAICS_72 = "72"
    NAICS_23 = "23"
    NAICS_31 = "31"
    NAICS_71 = "71"
    NAICS_51 = "51"
    NAICS_42 = "42"
    NAICS_45 = "45"
    NAICS_53 = "53"
    NAICS_48 = "48"
    NAICS_62 = "62"
    NAICS_21 = "21"
    NAICS_81 = "81"
    NAICS_52 = "52"
    NAICS_11 = "11"
    NAICS_49 = "49"
    NAICS_92 = "92"
    NAICS_55 = "55"
    NAICS_22 = "22"


class YesNoEnum(str, Enum):
    YES = "Y"
    NO = "N"


class Loan(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="loans")

    state: StateEnum = Field(nullable=False)
    bank: str = Field(nullable=False, index=True)  # Should be validated against a predefined list
    naics: NAICSEnum = Field(nullable=False)
    rev_line_cr: YesNoEnum = Field(nullable=False)
    low_doc: YesNoEnum = Field(nullable=False)
    
    new_exist: Optional[int] = Field(default=None)  # 0, 1, or null
    create_job: Optional[int] = Field(default=None)
    has_franchise: Optional[int] = Field(default=None)
    recession: Optional[int] = Field(default=None)
    urban_rural: Optional[int] = Field(default=None)
    retained_job: Optional[int] = Field(default=None)

    term: int = Field(nullable=False)
    no_emp: int = Field(nullable=False)
    gr_appv: float = Field(nullable=False)

    # Prediction Fields
    prediction: Optional[int] = Field(default=None)  # 0 or 1
    proba_yes: Optional[float] = Field(default=None)  # Between 0 and 1
    proba_no: Optional[float] = Field(default=None)  # Between 0 and 1
    shap_values: Optional[List[float]] = Field(default=None, sa_column=Column(JSON))

    def get_data(self) -> Dict:
        """
        Returns all loan-related data in a dictionary format.

        Returns:
            dict: A dictionary containing all loan attributes for make a prediction.
        """
        print("type : ", type(self.rev_line_cr.value))
        return {
            "State": self.state.value,
            "Bank": self.bank,
            "NAICS": self.naics.value,
            "Term": self.term,
            "NoEmp": self.no_emp,
            "NewExist": self.new_exist,
            "CreateJob": self.create_job,
            "RetainedJob": self.retained_job,
            "UrbanRural": self.urban_rural,
            "RevLineCr": str(self.rev_line_cr.value),
            "LowDoc": str(self.low_doc.value),
            "GrAppv": self.gr_appv,
            "Recession": self.recession,
            "HasFranchise": self.has_franchise
        }
    
    def make_prediction(self):
        with open('static/cat_boost_model.pkl', "rb") as f:
            model = cloudpickle.load(f)
        df = pd.DataFrame([self.get_data()])
        print(df)
        print(df.dtypes)
        self.prediction = model.predict(df)[0]
        proba = model.predict_proba(df)[0]
        self.proba_no = proba[0]
        self.proba_yes = proba[1]
        explainer = shap.TreeExplainer(model)
        self.shap_values = list(explainer.shap_values(df.iloc[[0]])[0])
