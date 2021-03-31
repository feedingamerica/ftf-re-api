from pandas.core.frame import DataFrame
import dateutil.parser as parser
import pandas as pd
from django.db import connections


from transform_layer.services.utils import date_str_to_int, get_control_query

import copy

SCOPE_HIERARCHY = "hierarchy"
SCOPE_GEOGRAPHY = "geography"

#1 instance of DataService for 1 scope
class DataService:

    def __init__(self, scope):
        self.scope = scope
        self._fact_services = None
        self._service_types = None
        self._family_services = None
        self._new_familiy_services = None 

    ## returns DataFrame for a specific data definition
    def get_data_for_definition(self, id):
        if id>=1 and id <= 22:
            if(self._fact_services) is None:
                self._fact_services = self.__get_fact_services()
            return self._fact_services
        elif id <= 25:
            if(self._service_types) is None:
                self._service_types = self.__get_service_types()
            return self._service_types
        elif id <= 31:
            if(self._family_services) is None:
                self._family_services = self.__get_family_services()
            return self._family_services
        elif id <= 45:
            if(self._new_familiy_services) is None:
                self._new_familiy_services = self.__get_new_family_services()
            return self._new_familiy_services


        ## retrieves fact_services
    def __get_fact_services(self):
        conn = connections['source_db']

        table1 = ""
        left1 = right1 = ""

        if self.scope["scope_type"] == "hierarchy":
            table1 = "dim_hierarchies"
            left1 = right1 = "hierarchy_id"
        elif self.scope["scope_type"] == "geography":
            table1 = "dim_geos"
            left1 = "dimgeo_id"
            right1 = "id"

        control_type_name = self.scope["control_type_name"]
        control_query = get_control_query(control_type_name)
        scope_field = self.scope["scope_field"]
        scope_value = self.scope["scope_field_value"]
        start_date = date_str_to_int(self.scope["startDate"])
        end_date = date_str_to_int(self.scope["endDate"])

        query = f"""
        SELECT
            fs.research_service_key,
            fs.{left1},
            fs.service_status,
            fs.service_id,
            fs.research_family_key,
            fs.served_children,
            fs.served_adults,
            fs.served_seniors,
            fs.served_total,
            fsm.research_member_key
        FROM 
            fact_services AS fs
            INNER JOIN dim_service_types ON fs.service_id = dim_service_types.id
            LEFT JOIN {table1} AS t1 ON fs.{left1} = t1.{right1}
            LEFT JOIN dim_service_statuses ON fs.service_status = dim_service_statuses.status 
            LEFT JOIN fact_service_members AS fsm ON fs.research_service_key = fsm.research_service_key
        WHERE
            fs.service_status = 17
            AND {control_query}
            AND t1.{scope_field} = {scope_value}
            AND fs.date >= {start_date} AND fs.date <= {end_date}
        """

        return pd.read_sql(query, conn)


    def __get_service_types(self):
        conn = connections['source_db']

        extra_join = ""
        if self.scope["scope_type"] == "hierarchy":
            table1 = "dim_hierarchies"
            left1 = right1 = "hierarchy_id"
        elif self.scope["scope_type"] == "geography":
            table1 = "dim_geos"
            left1 = "dimgeo_id"
            right1 = "id"
            extra_join = """INNER JOIN dim_hierarchies ON fact_services.hierarchy_id = dim_hierarchies.loc_id"""

        control_type_name = self.scope["control_type_name"]
        control_query = get_control_query(control_type_name)
        scope_field = self.scope["scope_field"]
        scope_value = self.scope["scope_field_value"]
        start_date = date_str_to_int(self.scope["startDate"])
        end_date = date_str_to_int(self.scope["endDate"])

        query = f"""
        SELECT
            fact_services.research_service_key,
            fact_services.research_family_key,
            fact_services.service_id,
            dim_service_types.name as service_name,
            dim_service_types.service_category_code,
            dim_service_types.service_category_name,
            fact_services.served_total,
            dim_hierarchies.loc_id
        FROM
            fact_services
            INNER JOIN dim_service_types ON fact_services.service_id = dim_service_types.id
            INNER JOIN {table1} ON fact_services.{left1} = {table1}.{right1}
            {extra_join if self.scope["scope_type"] == "geography" else ""}
        WHERE
            fact_services.service_status = 17 
            AND {control_query}
            AND fact_services.date >= {start_date} AND fact_services.date <= {end_date}
            AND {table1}.{scope_field} = {scope_value}
        """
        return pd.read_sql(query, conn)


    def __get_family_services(self):
        conn = connections['source_db']

        table1 = ""
        left1 = right1 = ""

        if self.scope["scope_type"] == "hierarchy":
            table1 = "dim_hierarchies"
            left1 = right1 = "hierarchy_id"
        elif self.scope["scope_type"] == "geography":
            table1 = "dim_geos"
            left1 = "dimgeo_id"
            right1 = "id"

        control_type_name = self.scope["control_type_name"]
        control_query = get_control_query(control_type_name)
        scope_field = self.scope["scope_field"]
        scope_value = self.scope["scope_field_value"]
        start_date = date_str_to_int(self.scope["startDate"])
        end_date = date_str_to_int(self.scope["endDate"])

        query = f"""
        SELECT
            fact_services.research_family_key,
            COUNT(fact_services.research_service_key) AS num_services,
            AVG(fact_services.served_total) AS avg_fam_size,
            SUM(fact_services.is_first_service_date) as timeframe_has_first_service_date,
            AVG(fact_services.days_since_first_service) AS avg_days_since_first_service,
            MAX(fact_services.days_since_first_service) AS max_days_since_first_service,
            dim_family_compositions.family_composition_type
        FROM 
            fact_services
            INNER JOIN dim_families ON fact_services.research_family_key = dim_families.research_family_key
            INNER JOIN dim_family_compositions ON dim_families.family_composition_type = dim_family_compositions.id
            INNER JOIN dim_service_types ON fact_services.service_id = dim_service_types.id
            INNER JOIN {table1}  ON fact_services.{left1} = {table1}.{right1}
        WHERE
            fact_services.service_status = 17 
            AND {control_query}
            AND fact_services.date >= {start_date} AND fact_services.date <= {end_date}
            AND {table1}.{scope_field} = {scope_value}
        GROUP BY
            fact_services.research_family_key,
            dim_family_compositions.family_composition_type
        """
        
        return pd.read_sql(query, conn)

    def __get_new_family_services(self):
        conn = connections['source_db']

        extra_join = ""
        if self.scope["scope_type"] == "hierarchy":
            table1 = "dim_hierarchies"
            left1 = right1 = "hierarchy_id"
        elif self.scope["scope_type"] == "geography":
            table1 = "dim_geos"
            left1 = "dimgeo_id"
            right1 = "id"
            extra_join = """INNER JOIN dim_hierarchies ON fs.hierarchy_id = dim_hierarchies.loc_id"""

        control_type_name = self.scope["control_type_name"]
        control_query = get_control_query(control_type_name)
        scope_field = self.scope["scope_field"]
        scope_value = self.scope["scope_field_value"]
        start_date = date_str_to_int(self.scope["startDate"])
        end_date = date_str_to_int(self.scope["endDate"])

        services_query = f"""
        SELECT
            fs.research_service_key,
            fs.research_family_key,
            fs.service_id,
            dim_service_types.name as service_name,
            dim_service_types.service_category_code,
            dim_service_types.service_category_name,
            fs.served_total,
            dim_hierarchies.loc_id,
            fs.is_first_service_date
        FROM
            fact_services AS fs
            INNER JOIN dim_service_types ON fs.service_id = dim_service_types.id
            INNER JOIN {table1} ON fs.{left1} = {table1}.{right1}
            INNER JOIN dim_dates ON fs.date = dim_dates.date_key
            {extra_join if self.scope["scope_type"] == "geography" else ""}
        WHERE
            fs.service_status = 17 
            AND {control_query}
            AND fs.date >= {start_date} AND fs.date <= {end_date}
            AND {table1}.{scope_field} = {scope_value}
        """

        families_query = f"""
            SELECT
                fs.research_family_key,
                COUNT( fs.research_service_key ) AS num_services,
                AVG( fs.served_total ) AS avg_fam_size,
                SUM( fs.is_first_service_date ) AS timeframe_has_first_service_date,
                AVG( fs.days_since_first_service ) AS avg_days_since_first_service,
                MAX( fs.days_since_first_service ) AS max_days_since_first_service,
                dim_family_compositions.family_composition_type,
                dim_families.datekey_first_service,
                dim_families.dummy_use_geo,
                dim_families.latitude_5,
                dim_families.longitude_5,
                dim_families.dimgeo_id,
                dim_geos.fips_state,
                dim_geos.fips_cnty,
                dim_geos.fips_zcta
            FROM
                fact_services AS fs
                INNER JOIN dim_families ON fs.research_family_key = dim_families.research_family_key
                INNER JOIN dim_family_compositions ON dim_families.family_composition_type = dim_family_compositions.id
                INNER JOIN dim_service_types ON fs.service_id = dim_service_types.id
                INNER JOIN dim_dates ON fs.date = dim_dates.date_key
                INNER JOIN {table1} ON fs.{left1} = {table1}.{right1}
                LEFT JOIN dim_geos ON dim_families.dimgeo_id = dim_geos.id
                {extra_join if self.scope["scope_type"] == "geography" else ""}
            WHERE
                fs.service_status = 17
                AND {control_query}
                AND fs.date >= {start_date} AND fs.date <= {end_date}
                AND {table1}.{scope_field} = {scope_value}
            GROUP BY
                fs.research_family_key,
                dim_family_compositions.family_composition_type,
                dim_families.datekey_first_service,
                dim_families.dummy_use_geo,
                dim_families.latitude_5,
                dim_families.longitude_5,
                dim_families.dimgeo_id,
                dim_geos.fips_state,
                dim_geos.fips_cnty,
                dim_geos.fips_zcta
        """

        members_query = f"""
        SELECT
            fs_mem.research_member_key,
            COUNT( fs.research_service_key ) AS num_services,
            SUM( fs_mem.is_first_service_date ) AS timeframe_has_first_service_date,
            AVG( fs_mem.days_since_first_service ) AS avg_days_since_first_service,
            MAX( fs_mem.days_since_first_service ) AS max_days_since_first_service,
            dim_members.datekey_first_served,
            dim_members.gender,
            dim_members.current_age,
            dim_members.race_id,
            dim_members.ethnic_id,
            dim_members.immigrant_id,
            dim_members.language_id,
            dim_members.disability_id,
            dim_members.military_id,
            dim_members.healthcare_id,
            dim_members.education_id,
            dim_members.employment_id,
            dim_families.datekey_first_service AS dim_families_datekey_first_service,
            SUM( fs.is_first_service_date ) AS dim_families_timeframe_has_first_service_date
        FROM
            fact_services AS fs
            INNER JOIN dim_service_types ON fs.service_id = dim_service_types.id
            INNER JOIN {table1} ON fs.{left1} = {table1}.{right1}
            INNER JOIN dim_dates ON fs.date = dim_dates.date_key
            INNER JOIN fact_service_members AS fs_mem ON fs.research_service_key = fs_mem.research_service_key
            INNER JOIN dim_members ON fs_mem.research_member_key = dim_members.research_member_key
            INNER JOIN dim_families ON dim_members.research_family_key = dim_families.research_family_key
            {extra_join if self.scope["scope_type"] == "geography" else ""}
        WHERE
            fs.service_status = 17
            AND {control_query}
            AND {table1}.{scope_field} = {scope_value}
            AND fs.date >= {start_date} AND fs.date <= {end_date}
        GROUP BY
            fs_mem.research_member_key
        """
        
        services = pd.read_sql(services_query, conn)
        families = pd.read_sql(families_query, conn)
        members = pd.read_sql(members_query, conn)
        
        ## TODO remove, for testing only
        print("SERVICES")
        print(services)
        print("FAMILIES")
        print(families)
        print("MEMBERS")
        print(members)

        return [services, families, members]