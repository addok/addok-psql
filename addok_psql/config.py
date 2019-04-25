PSQL = {
    'dbname': 'nominatim'
}
PSQL_PROCESSORS = (
    'addok_psql.processors.query',
    'addok_psql.processors.get_context',
    'addok_psql.processors.get_housenumbers',
    'addok_psql.processors.row_to_doc',
)
PSQL_QUERY = """SELECT osm_type,osm_id,class,type,admin_level,rank_search,
             place_id,parent_place_id,
             address->'street' as street,
             postcode,
             (extratags->'ref') as ref,
             ST_X(ST_Centroid(geometry)) as lon,
             ST_Y(ST_Centroid(geometry)) as lat,
             name->'name' as name, name->'short_name' as short_name,
             name->'official_name' as official_name,
             name->'alt_name' as alt_name
             FROM placex
             WHERE name ? 'name'
             {extrawhere}
             ORDER BY place_id
             {limit}
             """
PSQL_EXTRAWHERE = ''
# If you only want addresses
# PSQL_EXTRAWHERE = "AND class='highway' AND osm_type='W'"
# If you don't want any address
# PSQL_EXTRAWHERE = ("AND (class!='highway' OR osm_type='W') "
#                    "AND class!='place'")

PSQL_LIMIT = None
PSQL_ITERSIZE = 1000
