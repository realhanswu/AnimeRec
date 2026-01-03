from fastapi import Request, HTTPException

def get_rec_service(request: Request):
    # Debug print to see what's actually inside during the request
    # print(f"DEBUG: Checking state... keys: {request.app.state.ml_models.keys()}")

    # Check 1: Does the 'ml_models' dictionary exist?
    if not hasattr(request.app.state, "ml_models"):
        raise HTTPException(status_code=503, detail="State not initialized (No ml_models dict)")

    # Check 2: Is the service inside it?
    if "rec_service" not in request.app.state.ml_models:
        raise HTTPException(status_code=503, detail="Service not ready (rec_service key missing)")

    return request.app.state.ml_models["rec_service"]
