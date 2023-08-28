order_history_data_one = """
        SELECT ORDER_ORDR_NBR, CUSTOMER_NAME, ORDER_CHANNEL, PRODUCT_DESCRIPTION, ORDER_DATE, CTRY_HIER_DIM_CTRY, SHIPMENT_ORDR_TYP, ORDER_LINE_LINE_NBR
        FROM `imgcp-20220315135638.Prd_Repo.ORDERS`
        WHERE CUSTOMER_NAME = "EASTECH SYSTEMS LTD"
        ORDER BY ORDER_DATE DESC
        LIMIT 10000"""

product_data_one = """
        SELECT a.MATERIAL, MATERIALTYPE, a.CONTENTPROVIDER, ATTRIBUTEVALUE, ATTRIBUTEVALUE2, ABSOLUTEVALUE, ABSOLUTEVALUE_UNIT, SHORTDESCRIPTION
        FROM `imgcp-20220210133450.PIMCOREPROD.ATTRIBUTE_MD` a JOIN `imgcp-20220210133450.PIMCOREPROD.DESCRIPTION` b ON a.MATERIAL = b.MATERIAL LIMIT 1000
        """

# feel free to add your data_queries here
data_templates = {
    'order_data': [
        {"order_one": order_history_data_one}
    ],
    'product_data': [
        {"product_one": product_data_one}
    ]
}

product_master = """SELECT
  prod_inshed.CATALOG_NBR,
  prod_inshed.DESCRIPTION,
  prod_inshed.KEYWORD,
  prod_inshed.BASE_PRICE,
  prod_inshed.WEIGHT,
  category_main.CATEGORYNAME,
  vendor_main.WEBFRIENDLYNAME,
  pimcore_prod.LONGDESCRIPTION,
  pimcore_prod.SHORTDESCRIPTION
FROM
  `imgcp-20220210133450.ODSPROD.IMS_PROD_INSHED` prod_inshed
JOIN
  `imgcp-20220210133450.PIMCOREPROD.CATEGORY_MAIN` category_main
ON
  prod_inshed.CATEGORY = category_main.CATEGORYCODE
JOIN
  `imgcp-20220210133450.PIMCOREPROD.VENDOR_MAIN` vendor_main
ON
  prod_inshed.VENDOR_NBR = vendor_main.VENDORCODE
JOIN 
`imgcp-20220210133450.PIMCOREPROD.DESCRIPTION` pimcore_prod
ON
  pimcore_prod.VENDORPARTNUMBER = prod_inshed.VENDOR_PART_NBR
limit 1000000"""