def generate_cron_expression(interval, unit):
    # Handle unit:
    unit = unit.lower()
    unit = unit.split('_')[1]

    expression = None
    
    # Minutes
    if unit.lower() in ["minutes","minute"]:
        expression = f"*/{interval} * * * *"

    # Hours
    elif unit.lower() in ["hours","hour"]:
        expression = f"0 */{interval} * * *"

    # Days
    elif unit.lower() in ["days","day"]:
        expression = f"0 0 */{interval} * *"

    # Weeks
    elif unit.lower() in ["weeks","week"]:
        expression = f"0 0 */{interval*7} * *" # Bad way to do it but better then nothing

    # Months
    elif unit.lower() in ["months","month"]:
        expression = f"0 0 1 */{interval} 0" # Worse way to do it but works between 1 and 12
        if interval < 1 or interval > 12:
            raise ValueError("Crontab expressions for months must be between 1 and 12!")

    # Return
    if expression != None:
        return expression