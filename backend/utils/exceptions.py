"""
Custom exceptions for the application
"""


class ApplicationException(Exception):
    """Base exception for application errors"""
    pass


class FileUploadException(ApplicationException):
    """Exception for file upload errors"""
    pass


class InvalidFileFormatException(FileUploadException):
    """Exception for invalid file format"""
    pass


class FileSizeExceededException(FileUploadException):
    """Exception for file size exceeding limit"""
    pass


class ImageProcessingException(ApplicationException):
    """Exception for image processing errors"""
    pass


class VideoProcessingException(ApplicationException):
    """Exception for video processing errors"""
    pass


class ModelNotTrainedException(ApplicationException):
    """Exception when model is not trained"""
    pass


class DatabaseException(ApplicationException):
    """Exception for database errors"""
    pass


class ValidationException(ApplicationException):
    """Exception for validation errors"""
    pass


class ReportGenerationException(ApplicationException):
    """Exception for report generation errors"""
    pass
