-- Search table: String 
SELECT DISTINCT search_key FROM odc.dataset_search_string;

-- Search table: num
SELECT DISTINCT search_key FROM odc.dataset_search_num;

-- Find out what keys exist in properties
SELECT DISTINCT jsonb_object_keys(metadata->'properties') as property_key
FROM odc.dataset
ORDER BY property_key;
