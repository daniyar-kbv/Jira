import os
from django.core.exceptions import ValidationError

ALLOWED_EXTS = ['.jpg', '.png', '.docx']

def validate_file_size(value):
  if value.size > 5000000:
    raise ValidationError('max file size: 5Mb')

def validate_extension(value):
  ext = os.path.splitext(value.name)[1]
  if not ext.lower() in ALLOWED_EXTS:
    raise ValidationError(f'not allowed file ext, allowed: {ALLOWED_EXTS}')