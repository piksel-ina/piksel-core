-- scripts/delete_odc_product.sql
-- Set the search path to the odc schema so that all operations occur in the correct namespace.
SET search_path = odc;


-- Delete location records from spatial_9468
WITH datasets AS (
  SELECT id
  FROM dataset
  WHERE product_ref = (SELECT id FROM product WHERE name = :'product_name')
)
DELETE FROM spatial_9468
USING datasets
WHERE spatial_9468.dataset_ref = datasets.id;

-- Delete dataset records that reference the product
DELETE FROM dataset
WHERE product_ref = (SELECT id FROM product WHERE name = :'product_name');

-- Finally, delete the product definition itself
DELETE FROM product
WHERE name = :'product_name';

-- Optionally, drop any associated views and dynamic indexes if they exist
\set view_name 'dv_' :product_name '_dataset'
DROP VIEW IF EXISTS :view_name;

\set index_name 'dix_' :product_name '_%'
SELECT FORMAT('DROP INDEX CONCURRENTLY %I.%I;', schemaname, indexname) AS drop_statement
FROM pg_indexes 
WHERE tablename = 'dataset' AND indexname LIKE :'index_name'; \gexec
