import dateutil.parser as parser

def date_str_to_int(date):
    dt = parser.parse(date,dayfirst = False)
    date_int = (10000*dt.year)+ (100 * dt.month) + dt.day 
    return date_int


def get_control_query(control_type_name):
    if (control_type_name == "Prepack & Choice only"):
        return f"AND dim_service_types.service_category_code IN (10, 15)"
    elif (control_type_name == "Produce only"):
        return f"AND dim_service_types.service_category_code IN (20)"
    elif (control_type_name == "Everything"):
            #return f"dim_service_types.service_category_code LIKE '%' "
            return f""
    elif (control_type_name == "TEFAP"):
            return f'AND dim_service_types.name = "TEFAP"'
    else:
        return f"AND dim_service_types.dummy_is_grocery_service = 1"
