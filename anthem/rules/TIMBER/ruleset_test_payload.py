rule_json ={

  "rule_name": "test_810_2",
  "description": null,
  "rule_type": "exception",
  "start_date": "2022-07-28",
  "end_date": "9999-12-31",
  "scope": {
    "type": "custom",
    "sub-scope": "",
    "options": {
      "page_num": ""
    }
  },
  "conditions": [
    {
      "log": "and",
      "conditions": [
        {
          "op": "==",
          "rval": 85,
          "lval": "Charges",
          "json_path": "$.Claim.Lines"
        },
        {
          "op": "==",
          "rval": "99382",
          "lval": "Hcpcs",
          "json_path": "$.Claim.Lines"
        },
        {
          "op": "==",
          "rval": 1407842859,
          "lval": "RenderingNpi",
          "json_path": "$.Claim.Lines"
        },
        {
          "op": "==",
          "rval": 0.9145725967,
          "lval": "ModelScore",
          "json_path": "$.Propensity.Edits"
        },
        {
          "log": "or",
          "conditions": [
            {
              "op": "all",
              "rval": [
                "1770932337",
                "17709323414",
                "177093r32r32",
                "177093233rqrqw"
              ],
              "lval": "BillingNpi",
              "json_path": "$.Claim.Header"
            },
            {
              "op": "==",
              "rval": 85,
              "lval": "Charges",
              "json_path": "$.Claim.Lines"
            },
            {
              "op": "==",
              "rval": "99382",
              "lval": "Hcpcs",
              "json_path": "$.Claim.Lines"
            },
            {
              "op": "==",
              "rval": 1407842859,
              "lval": "RenderingNpi",
              "json_path": "$.Claim.Lines"
            },
            {
              "op": "==",
              "rval": "D",
              "lval": "ModelVersion",
              "json_path": "$.Propensity.Edits"
            },
            {
              "log": "or",
              "conditions": [
                {
                  "op": "==",
                  "rval": 85,
                  "lval": "Charges",
                  "json_path": "$.Claim.Lines"
                },
                {
                  "op": "==",
                  "rval": "99382",
                  "lval": "Hcpcs",
                  "json_path": "$.Claim.Lines"
                },
                {
                  "op": "==",
                  "rval": 1407842859,
                  "lval": "RenderingNpi",
                  "json_path": "$.Claim.Lines"
                },
                {
                  "op": "==",
                  "rval": 0.91,
                  "lval": "ModelScore",
                  "json_path": "$.Propensity.Edits"
                }
              ]
            }
          ]
        }
      ]
    }
  ],
  "actions": [
    {
      "json_path": "$.Messages",
      "op": "create_attribute_new",
      "lval": "EditDisposition",
      "rval": "UserIgnoreEdit",
      "action_type": "custom"
    }
  ],
  "solution_id": "claimsol3",
  "rule_id": "0f8666f6-ddeb-4d61-9ec5-9d4da35ac236_810_2",
  "version_seq": 2,
  "is_deleted": false,
  "created_ts": "2022-07-29 11:14:28.331633",
  "is_active": true,
  "rule_group": "Exclusion"
}


ruleset = {

  "rules": [
    "0f8666f6-ddeb-4d61-9ec5-9d4da35ac236_810_2"
  ],
  "name": "test_810",
  "solution_id": "claimsol3",
  "is_deleted": false,
  "is_enabled": true,
  "is_published": true,
  "created_by": "system",
  "modified_by": "system",
  "metadata": {
    "mode": "shadow",
    "clientID": "10001",
    "client_name": "ANTHEM",
    "lob": "WGS-CSBD",
    "EOBCode": "00W02"
  },
  "ruleset_id": "test_Sick_810",
  "ruleset_name": "test_sick_810",
  "sso_id": "AH85065",
  "client_id": "10001",
  "config_num": "0001",
  "lob": "WGS-CSBD",
  "description": "",
  "version_seq": 17,
  "created_ts": "2022-07-11 10:46:00.450230"
}


payload = """
{
  "header": {
    "msg_id": "1f29062f-a11e-461e-834b-6104b94ce557",
    "msg_type": "api",
    "from": "mqproxy",
    "to": "sync.api.get_rules",
    "timestamp": "2022-06-06T12:53:30.308785"
  },
  "payload": {
    "request_id": "57c212fb-96ba-4a62-8ec2-5fd09aebed06",
    "entity_name": "",
    "solution_id": "claimsol3",
    "trigger": "execute_rulesets",
    "primary_key": {
      
    },
    "context": {
      
    },
    "status": {
      "success": true,
      "code": 200,
      "message": "",
      "error_details": {
        
      },
      "traceback": ""
    },
    "data":{"Claim":{"Header":{"AcceptAssignment":"A","ActualPaidAmount":0,"AdjustmentBacterialPneumonia":"H","AdjustmentGiBleed":"H","AdjustmentOnsetDialysis":"H","AdjustmentOnsetDialysisStartDate":"H","AdjustmentPericarditis":"H","AdmissionDate":"00/00/0000","AdmissionDxCode":"","AmbulancePickupZip":"","BeneficiaryId":"B009W077402251984FDANNISHALAND","BeneficiaryZip":"31721","BillingNpi":["1770932337","177093234144"],"BillingTaxonomy":"","BillingZip":"31707","BirthDate":"02/25/1984","ClaimDrg":"","ClaimId":"22188EE6665","ClaimNumber":"22188EE6665","ConditionCode01":" ","ConditionCode02":" ","ConditionCode03":" ","ConditionCode04":" ","ConditionCode05":" ","DxCode01":"Z00129","DxCode02":null,"DxCode03":null,"DxCode04":null,"DxCode05":null,"DxCode06":"","DxCode07":"","DxCode08":"","DxCode09":"","DxCode10":"","DxCode11":"","DxCode12":"","DxCode13":"","DxCode14":"","DxCode15":"","DxCode16":"","DxCode17":"","DxCode18":"","DxCode19":"","DxCode20":"","DxCode21":"","DxCode22":"","DxCode23":"","DxCode24":"","DxCode25":"","FederalTaxId":"812643904","FromDate":"06/15/2022","HealthPlanId":"Q6A1","IcdVersionIndicator":"0","MedicalRecordNumber":"49858Z6674","OccurrenceCode01":" ","OccurrenceCode02":" ","OccurrenceCode03":" ","OccurrenceCode04":" ","OccurrenceCode05":" ","OccurrenceDate01":"00/00/0000","OccurrenceDate02":"00/00/0000","OccurrenceDate03":"00/00/0000","OccurrenceDate04":"00/00/0000","OccurrenceDate05":"00/00/0000","OccurrenceSpanCode01":" ","OccurrenceSpanCode02":" ","OccurrenceSpanCode03":" ","OccurrenceSpanCode04":" ","OccurrenceSpanCode05":" ","OccurrenceSpanCode06":" ","OccurrenceSpanCode07":" ","OccurrenceSpanCode08":" ","OccurrenceSpanCode09":" ","OccurrenceSpanFromDate01":"00/00/0000","OccurrenceSpanFromDate02":"00/00/0000","OccurrenceSpanFromDate03":"00/00/0000","OccurrenceSpanFromDate04":"00/00/0000","OccurrenceSpanFromDate05":"00/00/0000","OccurrenceSpanFromDate06":"00/00/0000","OccurrenceSpanFromDate07":"00/00/0000","OccurrenceSpanFromDate08":"00/00/0000","OccurrenceSpanFromDate09":"00/00/0000","OccurrenceSpanThruDate01":"00/00/0000","OccurrenceSpanThruDate02":"00/00/0000","OccurrenceSpanThruDate03":"00/00/0000","OccurrenceSpanThruDate04":"00/00/0000","OccurrenceSpanThruDate05":"00/00/0000","OccurrenceSpanThruDate06":"00/00/0000","OccurrenceSpanThruDate07":"00/00/0000","OccurrenceSpanThruDate08":"00/00/0000","OccurrenceSpanThruDate09":"00/00/0000","Oscar":"","PatientControlNumber":"","PatientDischargeStatus":0,"PresentOnAdmission01":"","PresentOnAdmission02":"","PresentOnAdmission03":"","PresentOnAdmission04":"","PresentOnAdmission05":"","PresentOnAdmission06":"","PresentOnAdmission07":"","PresentOnAdmission08":"","PresentOnAdmission09":"","PresentOnAdmission10":"","PrimaryCarePhysicianYnFlag":"","PxCode01":" ","PxCode02":" ","PxCode03":" ","PxCode04":" ","PxCode05":" ","PxCode06":" ","PxCode07":" ","PxCode08":" ","PxCode09":" ","PxCode10":" ","PxCode11":" ","PxCode12":" ","PxCode13":" ","PxCode14":" ","PxCode15":" ","PxCode16":" ","PxCode17":" ","PxCode18":" ","PxCode19":" ","PxCode20":" ","PxCode21":" ","PxCode22":" ","PxCode23":" ","PxCode24":" ","PxCode25":" ","ReasonForVisitDxCode01":" ","ReasonForVisitDxCode02":" ","ReasonForVisitDxCode03":" ","ServiceFacilityZip":"","Sex":"F","SourceOfAdmission":"","ThruDate":"06/15/2022","TotalCharges":235,"TreatmentAuthorizationCode":"","TypeOfBill":"","ValueAmount01":0,"ValueAmount02":0,"ValueAmount03":0,"ValueAmount04":0,"ValueCode01":" ","ValueCode02":" ","ValueCode03":" ","ValueCode04":" ","PricingZipState":"GA","CaseNumber":"1770932337","PatientAge":"038","ProvSpcltyCd":"275","GroupNumber":"GA8039H1CC","MDCR_MDCD_CSBD_IND":"C","ClaimType":"PROF"},"Lines":[{"LineNumber":1,"Charges":150,"DateOfService":"06/15/2022","DxPointer":"1-0-0-0-0","DxPointer01":"Z00129","DxPointer02":"","DxPointer03":"","DxPointer04":"","DxPointer05":"","EndDateOfService":"06/15/2022","Hcpcs":"99201","Modifier01":"25","Modifier02":"CS","Modifier03":"","Modifier04":"","Modifier05":"","NationalDrugCode":"","NdcQualifier":"","NdcQuantity":0,"PlaceOfService":11,"RevenueCode":0,"Units":1,"AllowedAmount":"43.16","RenderingNpi":1407842859,"RenderingTaxonomy":"207R00000X"},{"LineNumber":2,"Charges":85,"DateOfService":"06/15/2022","DxPointer":"1-0-0-0-0","DxPointer01":"Z20822","DxPointer02":"","DxPointer03":"","DxPointer04":"","DxPointer05":"","EndDateOfService":"06/15/2022","Hcpcs":"99201","Modifier01":"CS","Modifier02":"","Modifier03":"","Modifier04":"","Modifier05":"","NationalDrugCode":"","NdcQualifier":"","NdcQuantity":0,"PlaceOfService":11,"RevenueCode":0,"Units":1,"AllowedAmount":"25.3","RenderingNpi":1407842859,"RenderingTaxonomy":"207R00000X"},{"LineNumber":3,"Charges":85,"DateOfService":"06/15/2022","DxPointer":"1-0-0-0-0","DxPointer01":"Z20822","DxPointer02":"","DxPointer03":"","DxPointer04":"","DxPointer05":"","EndDateOfService":"06/15/2022","Hcpcs":"99382","Modifier01":"CS","Modifier02":"","Modifier03":"","Modifier04":"","Modifier05":"","NationalDrugCode":"","NdcQualifier":"","NdcQuantity":0,"PlaceOfService":11,"RevenueCode":0,"Units":1,"AllowedAmount":"25.3","RenderingNpi":1407842859,"RenderingTaxonomy":"207R00000X"},{"LineNumber":4,"Charges":85,"DateOfService":"06/15/2022","DxPointer":"1-0-0-0-0","DxPointer01":"Z20822","DxPointer02":"","DxPointer03":"","DxPointer04":"","DxPointer05":"","EndDateOfService":"06/15/2022","Hcpcs":"95555","Modifier01":"CS","Modifier02":"","Modifier03":"","Modifier04":"","Modifier05":"","NationalDrugCode":"","NdcQualifier":"","NdcQuantity":0,"PlaceOfService":11,"RevenueCode":0,"Units":1,"AllowedAmount":"25.3","RenderingNpi":1407842859,"RenderingTaxonomy":"207R00000X"}]},"Envelope":{"UserId":"","ClientSystemId":"WGS","ClientTransactionId":"20210605201012TMBS21156BO125380999","ConfigurationNumber":"1044","MessageMappingId":"WGS","ProcessingMode":"Process"},"Propensity":{"Edits":[{"EditId":"PSMEM000001","ClaimNumber":"22188EE6665","ClaimLineNumber":"01","SourceCode":"CSBDD","ModelID":"EM.EPOV.P.CSBD","ModelVersion":"D","ModelScore":0.9145725967,"ModelScoreDateTime":"07/08/2022 14:49:39.739","FlaggingReason":"Upcoding","CrossReferenceClaim":null,"Parameters":[{"Name":"EPOVOutlierStatus","Value":"N"}]},{"EditId":"PSMEM000001","ClaimNumber":"22188EE6665","ClaimLineNumber":"02","SourceCode":"CSBDD","ModelID":"EM.EPOV.P.CSBD","ModelVersion":"D","ModelScore":0.9145725967,"ModelScoreDateTime":"07/08/2022 14:49:39.739","FlaggingReason":"Upcoding","CrossReferenceClaim":null,"Parameters":[{"Name":"EPOVOutlierStatus","Value":"N"}]},{"EditId":"PSMEM000001","ClaimNumber":"22188EE6665","ClaimLineNumber":"03","SourceCode":"CSBD","ModelID":"EM.EPOV.P.CSBD","ModelVersion":"D","ModelScore":0.91,"ModelScoreDateTime":"07/08/2022 14:49:39.739","FlaggingReason":"Upcoding","CrossReferenceClaim":null,"Parameters":[{"Name":"EPOVOutlierStatus","Value":"N"}]},{"EditId":"PSMEM000001","ClaimNumber":"22188EE6665","ClaimLineNumber":"04","SourceCode":"GBD","ModelID":"EM.EPOV.P.CSBD","ModelVersion":"D","ModelScore":0.91,"ModelScoreDateTime":"07/08/2022 14:49:39.739","FlaggingReason":"Upcoding","CrossReferenceClaim":null,"Parameters":[{"Name":"EPOVOutlierStatus","Value":"N"}]}]},"rule_based":true,"pred_models":true,"ruleset_filter":[{"ruleset_id":"test_Sick_810","client_id":"10001","config_num":"0001","run_all_exclusions":true}],"request_type":"execute_rulesets"}
    , "metadata": {      
    },
    "state": {
      "solution_group": "sync",
      "sync": true
    },
    "entity_id": ""
  }
}
"""