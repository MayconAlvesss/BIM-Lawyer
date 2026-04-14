class BIMLawyerException(Exception):
    """Base exception for all BIM-Lawyer errors."""
    pass

class AuditError(BIMLawyerException):
    """Raised when an audit fails to process."""
    pass

class NormNotFoundError(BIMLawyerException):
    """Raised when a specific regulation or clause is missing from the database."""
    pass

class GeometryProcessingError(BIMLawyerException):
    """Raised when Revit geometry strings cannot be parsed."""
    pass

class UnauthorizedAuditRequest(BIMLawyerException):
    """Raised when API key or roles are insufficient."""
    pass
