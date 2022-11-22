from django.core.exceptions import ValidationError

def cv_validator(cv_file):
    file = str(cv_file)
    file_accepted=file.endswith(".pdf") or file.endswith(".docx") or file.endswith(".doc")
    print(file_accepted)
    if not file_accepted:
        raise ValidationError("Only cv files in the pdf or doc formats can be uploaded")
    return cv_file
    