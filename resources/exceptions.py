class UnauthorizedError(Exception):
    pass


errors = {
    "UnauthorizedError": {
        "message": "Invalid username/password/token",
        "status": 401
    }
}
