from django.db import migrations

update_config = """
        update nodes set exportable = false, fieldname = 'heritheme' where nodeid = '08e4e0fe-cd71-11ed-bcae-5254004d77d3'; --Heritage Theme
        update nodes set exportable = false, fieldname = '' where nodeid = '0684fec8-0d07-11ed-8804-5254008afee6'; --Site Record Admin
        update nodes set exportable = false, fieldname = 'srcnts' where nodeid = '05831728-c6d6-11ee-a8fd-080027b7463b'; --Source Notes
        update nodes set exportable = false, fieldname = 'photograph' where nodeid = '15f8f37c-2fc2-11ed-9cc9-5254008afee6'; --Photographer
        update nodes set exportable = false, fieldname = 'image_view' where nodeid = '020c98ae-4427-11ed-8c76-5254008afee6'; --Image View
        update nodes set exportable = false, fieldname = 'copyright' where nodeid = '28009db8-2fc2-11ed-a26e-5254008afee6'; --Copyright
        update nodes set exportable = true, fieldname = 'CITY' where nodeid = '1b624082-0d0f-11ed-98c2-5254008afee6'; --City
        update nodes set exportable = false, fieldname = '' where nodeid = '1b62393e-0d0f-11ed-98c2-5254008afee6'; --Heritage Site Location
        update nodes set exportable = false, fieldname = null where nodeid = '611029e8-8f11-11ee-976b-080027b7463b'; --CRHP Admin
        update nodes set exportable = false, fieldname = '' where nodeid = '6cc30064-0d06-11ed-8804-5254008afee6'; --Protection Event
        update nodes set exportable = true, fieldname = 'RFRNC_NMBR' where nodeid = '6cc30b36-0d06-11ed-8804-5254008afee6'; --Reference Number
        update nodes set exportable = false, fieldname = 'desig_note' where nodeid = '6cc30c44-0d06-11ed-8804-5254008afee6'; --Protection Notes
        update nodes set exportable = true, fieldname = 'ST_NM_TYP' where nodeid = 'fa3a8094-0d05-11ed-8804-5254008afee6'; --Name Type
        update nodes set exportable = false, fieldname = '' where nodeid = '6cc30474-0d06-11ed-8804-5254008afee6'; --BC Right
        update nodes set exportable = false, fieldname = null where nodeid = '19d560d2-0d05-11ed-a4d8-5254008afee6'; --Heritage Site
        update nodes set exportable = false, fieldname = null where nodeid = '7599be12-0d06-11ed-a4d8-5254008afee6'; --Heritage Class
        update nodes set exportable = false, fieldname = 'childsite' where nodeid = '0a5469a4-9eb4-11ee-b8bf-080027b7463b'; --Child Sites
        update nodes set exportable = false, fieldname = null where nodeid = '1b622ab6-0d0f-11ed-98c2-5254008afee6'; --BC Property Legal Description
        update nodes set exportable = true, fieldname = 'PID' where nodeid = 'ab6cb89e-d048-11ee-8370-080027b7463b'; --PID
        update nodes set exportable = false, fieldname = 'sitedoc' where nodeid = 'dc12f414-0d07-11ed-8804-5254008afee6'; --Site Document
        update nodes set exportable = false, fieldname = 'datesubmit' where nodeid = 'bb294f88-8f14-11ee-aaf0-080027b7463b'; --Date Submitted to CRHP
        update nodes set exportable = true, fieldname = 'OFFCLLY_RD' where nodeid = 'd2d91b6a-dfb3-11ed-b47a-5254004d77d3'; --Officially Recognized Site
        update nodes set exportable = false, fieldname = 'image_feat' where nodeid = 'e0f66da2-dfb2-11ed-b3d0-5254004d77d3'; --Image Features
        update nodes set exportable = false, fieldname = 'crhp_image' where nodeid = 'c27cb7c4-6d32-11ee-a6f7-080027b7463b'; --Submit to CRHP
        update nodes set exportable = false, fieldname = '' where nodeid = '6cc30e6a-0d06-11ed-8804-5254008afee6'; --Timespan of Designation or Protection
        update nodes set exportable = false, fieldname = 'legaldesc' where nodeid = '1b623ccc-0d0f-11ed-98c2-5254008afee6'; --Legal Description
        update nodes set exportable = true, fieldname = 'PROVINCE' where nodeid = '1b62419a-0d0f-11ed-98c2-5254008afee6'; --Province
        update nodes set exportable = false, fieldname = null where nodeid = 'fdd1b2ca-cd78-11ed-b7b5-5254004d77d3'; --Construction Actors
        update nodes set exportable = false, fieldname = 'image_desc' where nodeid = '9fa806e4-95ec-11ee-9e13-080027b7463b'; --Image Description
        update nodes set exportable = false, fieldname = 'doctype' where nodeid = 'f77e8d84-37b9-11ee-95f8-080027b7463b'; --Document Type
        update nodes set exportable = false, fieldname = 'imagetype' where nodeid = 'e82084a6-2fc1-11ed-8a32-5254008afee6'; --Image Type
        update nodes set exportable = true, fieldname = 'SITE_NAME' where nodeid = 'b5cdfd32-0d05-11ed-8804-5254008afee6'; --Name
        update nodes set exportable = false, fieldname = 'bcrstatus' where nodeid = '167e3e88-98a3-11ee-a464-080027b7463b'; --BCRHP Submission Status
        update nodes set exportable = false, fieldname = 'urltype' where nodeid = '1f5a7b92-ca41-11ed-933f-5254004d77d3'; --External URL Type
        update nodes set exportable = false, fieldname = '' where nodeid = '1b622e58-0d0f-11ed-98c2-5254008afee6'; --BC Property Address
        update nodes set exportable = false, fieldname = 'docdesc' where nodeid = '9be15b6a-ccc9-11ed-b7b5-5254004d77d3'; --Document Description
        update nodes set exportable = true, fieldname = 'EVENT' where nodeid = '98347640-cd88-11ed-bda2-5254004d77d3'; --Chronology
        update nodes set exportable = false, fieldname = 'image_date' where nodeid = '949eb98c-2fc2-11ed-ac88-5254008afee6'; --Image Date
        update nodes set exportable = true, fieldname = 'RSRC_CNT' where nodeid = '7599c3ee-0d06-11ed-a4d8-5254008afee6'; --Contributing Resource Count
        update nodes set exportable = false, fieldname = 'ownership' where nodeid = '7599c524-0d06-11ed-a4d8-5254008afee6'; --Ownership
        update nodes set exportable = false, fieldname = 'sosdescrip' where nodeid = '7a17162e-0d06-11ed-b43a-5254008afee6'; --Physical Description
        update nodes set exportable = false, fieldname = 'sosdocloc' where nodeid = '7a17173c-0d06-11ed-b43a-5254008afee6'; --Document Location
        update nodes set exportable = false, fieldname = 'sostype' where nodeid = '7a171840-0d06-11ed-b43a-5254008afee6'; --Significance Type
        update nodes set exportable = false, fieldname = 'soscdf' where nodeid = '7a1714f8-0d06-11ed-b43a-5254008afee6'; --Defining Elements
        update nodes set exportable = true, fieldname = 'EVNT_ST_YR' where nodeid = '727808be-cdaa-11ed-9868-5254004d77d3'; --Start Year
        update nodes set exportable = false, fieldname = null where nodeid = '7a171192-0d06-11ed-b43a-5254008afee6'; --BC Statement of Significance
        update nodes set exportable = true, fieldname = 'boundary' where nodeid = '1b6235b0-0d0f-11ed-98c2-5254008afee6'; --Site Boundary
        update nodes set exportable = true, fieldname = 'CATEGORY' where nodeid = '7599c628-0d06-11ed-a4d8-5254008afee6'; --Heritage Category
        update nodes set exportable = false, fieldname = 'accuracyrm' where nodeid = '1b6259fa-0d0f-11ed-98c2-5254008afee6'; --Accuracy Remarks
        update nodes set exportable = true, fieldname = 'EVNT_ND_YR' where nodeid = '406309d6-cdab-11ed-879a-5254004d77d3'; --End Year
        update nodes set exportable = true, fieldname = 'BLDR_TYP' where nodeid = '5fcd016e-cd79-11ed-a9fd-5254004d77d3'; --Construction Actor Type
        update nodes set exportable = true, fieldname = 'CIRCA' where nodeid = '42359120-6d24-11ee-a15e-080027b7463b'; --Dates Approximate
        update nodes set exportable = true, fieldname = 'RCGNTN_GVT' where nodeid = '50c26f28-3b93-11ee-ac05-080027b7463b'; --Responsible Government
        update nodes set exportable = true, fieldname = 'LOCALITY' where nodeid = '428ee192-8829-11ee-b6ec-080027b7463b'; --Locality
        update nodes set exportable = true, fieldname = 'RGSTRTN_SS' where nodeid = '44d59d3a-3d1d-11ee-9c2a-080027b7463b'; --Registration Status
        update nodes set exportable = true, fieldname = 'RCGNTN_ST' where nodeid = '6cc30f6e-0d06-11ed-8804-5254008afee6'; --Designation or Protection Start Date
        update nodes set exportable = true, fieldname = 'RCGNTN_END' where nodeid = '6cc30d5c-0d06-11ed-8804-5254008afee6'; --Designation or Protection End Date
        update nodes set exportable = true, fieldname = 'BLDR_NMS' where nodeid = '297eb4cc-cd79-11ed-9afb-5254004d77d3'; --Construction Actor
        update nodes set exportable = false, fieldname = null where nodeid = '531c8ff8-cdaa-11ed-8c2b-5254004d77d3'; --Event Period
        update nodes set exportable = false, fieldname = 'url' where nodeid = '3ee73f28-ca40-11ed-af48-5254004d77d3'; --External URL
        update nodes set exportable = false, fieldname = 'prim_image' where nodeid = '703bbe62-3d24-11ee-93bd-080027b7463b'; --Primary Image
        update nodes set exportable = true, fieldname = 'LEG_ACT' where nodeid = '1f28339e-3b93-11ee-b4c5-080027b7463b'; --Legislative Act
        update nodes set exportable = false, fieldname = null where nodeid = '32d004b6-0d05-11ed-a4d8-5254008afee6'; --Site Names
        update nodes set exportable = true, fieldname = 'RGSTRY_TYP' where nodeid = '8e61e1bc-2495-11ed-8f55-5254008afee6'; --Registry Types
        update nodes set exportable = false, fieldname = 'PIN' where nodeid = 'e1f9e6b6-d048-11ee-8370-080027b7463b'; --PIN
        update nodes set exportable = true, fieldname = 'LOC_DESC' where nodeid = 'a1032cd8-1a66-11ed-a3cf-5254008afee6'; --Location Description
        update nodes set exportable = false, fieldname = 'remarkdate' where nodeid = '8e26b50e-9ae3-11ee-a366-080027b7463b'; --Remark Date
        update nodes set exportable = false, fieldname = 'remarktype' where nodeid = '8e26b69e-9ae3-11ee-a366-080027b7463b'; --Remark Type
        update nodes set exportable = false, fieldname = 'remark' where nodeid = '8e26b0a4-9ae3-11ee-a366-080027b7463b'; --Internal Remark
        update nodes set exportable = true, fieldname = 'FNCT_STTS' where nodeid = '89588ca2-0d07-11ed-a4d8-5254008afee6'; --Functional State
        update nodes set exportable = false, fieldname = 'datenotes' where nodeid = 'e470bafa-cdab-11ed-83b5-5254004d77d3'; --Chronology Notes
        update nodes set exportable = false, fieldname = 'Buildnotes' where nodeid = '84b27c34-cd79-11ed-9095-5254004d77d3'; --Construction Actor Notes
        update nodes set exportable = false, fieldname = 'datesource' where nodeid = '945eccb4-cdab-11ed-849b-5254004d77d3'; --Information Source
        update nodes set exportable = false, fieldname = 'soshv' where nodeid = '7a17193a-0d06-11ed-b43a-5254008afee6'; --Heritage Value
        update nodes set exportable = true, fieldname = 'FUNCTION' where nodeid = '89588b58-0d07-11ed-a4d8-5254008afee6'; --Functional Category
        update nodes set exportable = false, fieldname = 'restricted' where nodeid = 'dc974e68-8f0f-11ee-85a0-080027b7463b'; --Restricted
        update nodes set exportable = false, fieldname = 'crsubstat' where nodeid = 'af750d9c-8f11-11ee-976b-080027b7463b'; --CRHP Submission Status
        update nodes set exportable = false, fieldname = null where nodeid = '895887a2-0d07-11ed-a4d8-5254008afee6'; --Heritage Function
        update nodes set exportable = false, fieldname = 'postalcode' where nodeid = '1b625414-0d0f-11ed-98c2-5254008afee6'; --Postal Code
        update nodes set exportable = false, fieldname = 'LGLADDNOTE' where nodeid = '15656a28-1a67-11ed-b83c-5254008afee6'; --Legal Address Internal Notes
        update nodes set exportable = false, fieldname = 'fedid' where nodeid = '1eb0d10c-8f15-11ee-b395-080027b7463b'; --Federal ID Number
        update nodes set exportable = false, fieldname = 'ST_IMGS' where nodeid = '0a883b80-2fb6-11ed-be5f-5254008afee6'; --Site Images
        update nodes set exportable = true, fieldname = 'STRT_DDRSS' where nodeid = '1b624e60-0d0f-11ed-98c2-5254008afee6'; --Street Address
        update nodes set exportable = true, fieldname = 'BRDNNMBR' where nodeid = 'e5ecf044-0d06-11ed-86c8-5254008afee6'; --Borden Number

    """

# This is taken from TEST
revert_config = """
        update nodes set exportable = true, fieldname = 'image_view' where nodeid = '020c98ae-4427-11ed-8c76-5254008afee6'; --Image View
        update nodes set exportable = true, fieldname = 'srcnts' where nodeid = '05831728-c6d6-11ee-a8fd-080027b7463b'; --Source Notes
        update nodes set exportable = false, fieldname = '' where nodeid = '0684fec8-0d07-11ed-8804-5254008afee6'; --Site Record Admin
        update nodes set exportable = true, fieldname = 'heritheme' where nodeid = '08e4e0fe-cd71-11ed-bcae-5254004d77d3'; --Heritage Theme
        update nodes set exportable = true, fieldname = 'childsite' where nodeid = '0a5469a4-9eb4-11ee-b8bf-080027b7463b'; --Child Sites
        update nodes set exportable = true, fieldname = 'ST_IMGS' where nodeid = '0a883b80-2fb6-11ed-be5f-5254008afee6'; --Site Images
        update nodes set exportable = true, fieldname = 'LGLADDNOTE' where nodeid = '15656a28-1a67-11ed-b83c-5254008afee6'; --Legal Address Internal Notes
        update nodes set exportable = true, fieldname = 'photograph' where nodeid = '15f8f37c-2fc2-11ed-9cc9-5254008afee6'; --Photographer
        update nodes set exportable = true, fieldname = 'bcrstatus' where nodeid = '167e3e88-98a3-11ee-a464-080027b7463b'; --BCRHP Submission Status
        update nodes set exportable = false, fieldname = null where nodeid = '19d560d2-0d05-11ed-a4d8-5254008afee6'; --Heritage Site
        update nodes set exportable = false, fieldname = null where nodeid = '1b622ab6-0d0f-11ed-98c2-5254008afee6'; --BC Property Legal Description
        update nodes set exportable = false, fieldname = '' where nodeid = '1b622e58-0d0f-11ed-98c2-5254008afee6'; --BC Property Address
        update nodes set exportable = true, fieldname = 'boundary' where nodeid = '1b6235b0-0d0f-11ed-98c2-5254008afee6'; --Site Boundary
        update nodes set exportable = false, fieldname = '' where nodeid = '1b62393e-0d0f-11ed-98c2-5254008afee6'; --Heritage Site Location
        update nodes set exportable = true, fieldname = 'legaldesc' where nodeid = '1b623ccc-0d0f-11ed-98c2-5254008afee6'; --Legal Description
        update nodes set exportable = true, fieldname = 'city' where nodeid = '1b624082-0d0f-11ed-98c2-5254008afee6'; --City
        update nodes set exportable = true, fieldname = 'province' where nodeid = '1b62419a-0d0f-11ed-98c2-5254008afee6'; --Province
        update nodes set exportable = true, fieldname = 'address' where nodeid = '1b624e60-0d0f-11ed-98c2-5254008afee6'; --Street Address
        update nodes set exportable = true, fieldname = 'postalcode' where nodeid = '1b625414-0d0f-11ed-98c2-5254008afee6'; --Postal Code
        update nodes set exportable = true, fieldname = 'accuracyrm' where nodeid = '1b6259fa-0d0f-11ed-98c2-5254008afee6'; --Accuracy Remarks
        update nodes set exportable = true, fieldname = 'fedid' where nodeid = '1eb0d10c-8f15-11ee-b395-080027b7463b'; --Federal ID Number
        update nodes set exportable = true, fieldname = 'legact' where nodeid = '1f28339e-3b93-11ee-b4c5-080027b7463b'; --Legislative Act
        update nodes set exportable = true, fieldname = 'urltype' where nodeid = '1f5a7b92-ca41-11ed-933f-5254004d77d3'; --External URL Type
        update nodes set exportable = true, fieldname = 'copyright' where nodeid = '28009db8-2fc2-11ed-a26e-5254008afee6'; --Copyright
        update nodes set exportable = true, fieldname = 'Builder' where nodeid = '297eb4cc-cd79-11ed-9afb-5254004d77d3'; --Construction Actor
        update nodes set exportable = false, fieldname = null where nodeid = '32d004b6-0d05-11ed-a4d8-5254008afee6'; --Site Names
        update nodes set exportable = true, fieldname = 'url' where nodeid = '3ee73f28-ca40-11ed-af48-5254004d77d3'; --External URL
        update nodes set exportable = true, fieldname = 'chendyear' where nodeid = '406309d6-cdab-11ed-879a-5254004d77d3'; --End Year
        update nodes set exportable = true, fieldname = 'dateapprox' where nodeid = '42359120-6d24-11ee-a15e-080027b7463b'; --Dates Approximate
        update nodes set exportable = true, fieldname = 'locality' where nodeid = '428ee192-8829-11ee-b6ec-080027b7463b'; --Locality
        update nodes set exportable = true, fieldname = 'regstatus' where nodeid = '44d59d3a-3d1d-11ee-9c2a-080027b7463b'; --Registration Status
        update nodes set exportable = true, fieldname = 'government' where nodeid = '50c26f28-3b93-11ee-ac05-080027b7463b'; --Responsible Government
        update nodes set exportable = false, fieldname = null where nodeid = '531c8ff8-cdaa-11ed-8c2b-5254004d77d3'; --Event Period
        update nodes set exportable = true, fieldname = 'buildtype' where nodeid = '5fcd016e-cd79-11ed-a9fd-5254004d77d3'; --Construction Actor Type
        update nodes set exportable = false, fieldname = null where nodeid = '611029e8-8f11-11ee-976b-080027b7463b'; --CRHP Admin
        update nodes set exportable = false, fieldname = '' where nodeid = '6cc30064-0d06-11ed-8804-5254008afee6'; --Protection Event
        update nodes set exportable = false, fieldname = '' where nodeid = '6cc30474-0d06-11ed-8804-5254008afee6'; --BC Right
        update nodes set exportable = true, fieldname = 'refnum' where nodeid = '6cc30b36-0d06-11ed-8804-5254008afee6'; --Reference Number
        update nodes set exportable = true, fieldname = 'desig_note' where nodeid = '6cc30c44-0d06-11ed-8804-5254008afee6'; --Protection Notes
        update nodes set exportable = true, fieldname = 'desigend' where nodeid = '6cc30d5c-0d06-11ed-8804-5254008afee6'; --Designation or Protection End Date
        update nodes set exportable = false, fieldname = '' where nodeid = '6cc30e6a-0d06-11ed-8804-5254008afee6'; --Timespan of Designation or Protection
        update nodes set exportable = true, fieldname = 'desigstart' where nodeid = '6cc30f6e-0d06-11ed-8804-5254008afee6'; --Designation or Protection Start Date
        update nodes set exportable = true, fieldname = 'prim_image' where nodeid = '703bbe62-3d24-11ee-93bd-080027b7463b'; --Primary Image
        update nodes set exportable = true, fieldname = 'startyear' where nodeid = '727808be-cdaa-11ed-9868-5254004d77d3'; --Start Year
        update nodes set exportable = false, fieldname = null where nodeid = '7599be12-0d06-11ed-a4d8-5254008afee6'; --Heritage Class
        update nodes set exportable = true, fieldname = 'class_reso' where nodeid = '7599c3ee-0d06-11ed-a4d8-5254008afee6'; --Contributing Resource Count
        update nodes set exportable = true, fieldname = 'ownership' where nodeid = '7599c524-0d06-11ed-a4d8-5254008afee6'; --Ownership
        update nodes set exportable = true, fieldname = 'category' where nodeid = '7599c628-0d06-11ed-a4d8-5254008afee6'; --Heritage Category
        update nodes set exportable = false, fieldname = null where nodeid = '7a171192-0d06-11ed-b43a-5254008afee6'; --BC Statement of Significance
        update nodes set exportable = true, fieldname = 'soscdf' where nodeid = '7a1714f8-0d06-11ed-b43a-5254008afee6'; --Defining Elements
        update nodes set exportable = true, fieldname = 'sosdescrip' where nodeid = '7a17162e-0d06-11ed-b43a-5254008afee6'; --Physical Description
        update nodes set exportable = true, fieldname = 'sosdocloc' where nodeid = '7a17173c-0d06-11ed-b43a-5254008afee6'; --Document Location
        update nodes set exportable = true, fieldname = 'sostype' where nodeid = '7a171840-0d06-11ed-b43a-5254008afee6'; --Significance Type
        update nodes set exportable = true, fieldname = 'soshv' where nodeid = '7a17193a-0d06-11ed-b43a-5254008afee6'; --Heritage Value
        update nodes set exportable = true, fieldname = 'Buildnotes' where nodeid = '84b27c34-cd79-11ed-9095-5254004d77d3'; --Construction Actor Notes
        update nodes set exportable = false, fieldname = null where nodeid = '895887a2-0d07-11ed-a4d8-5254008afee6'; --Heritage Function
        update nodes set exportable = true, fieldname = 'funct_cat' where nodeid = '89588b58-0d07-11ed-a4d8-5254008afee6'; --Functional Category
        update nodes set exportable = true, fieldname = 'func_state' where nodeid = '89588ca2-0d07-11ed-a4d8-5254008afee6'; --Functional State
        update nodes set exportable = true, fieldname = 'remark' where nodeid = '8e26b0a4-9ae3-11ee-a366-080027b7463b'; --Internal Remark
        update nodes set exportable = true, fieldname = 'remarkdate' where nodeid = '8e26b50e-9ae3-11ee-a366-080027b7463b'; --Remark Date
        update nodes set exportable = true, fieldname = 'remarktype' where nodeid = '8e26b69e-9ae3-11ee-a366-080027b7463b'; --Remark Type
        update nodes set exportable = true, fieldname = 'regtype' where nodeid = '8e61e1bc-2495-11ed-8f55-5254008afee6'; --Registry Types
        update nodes set exportable = true, fieldname = 'datesource' where nodeid = '945eccb4-cdab-11ed-849b-5254004d77d3'; --Information Source
        update nodes set exportable = true, fieldname = 'image_date' where nodeid = '949eb98c-2fc2-11ed-ac88-5254008afee6'; --Image Date
        update nodes set exportable = true, fieldname = 'event' where nodeid = '98347640-cd88-11ed-bda2-5254004d77d3'; --Chronology
        update nodes set exportable = true, fieldname = 'docdesc' where nodeid = '9be15b6a-ccc9-11ed-b7b5-5254004d77d3'; --Document Description
        update nodes set exportable = true, fieldname = 'image_desc' where nodeid = '9fa806e4-95ec-11ee-9e13-080027b7463b'; --Image Description
        update nodes set exportable = true, fieldname = 'locdesc' where nodeid = 'a1032cd8-1a66-11ed-a3cf-5254008afee6'; --Location Description
        update nodes set exportable = true, fieldname = 'PID' where nodeid = 'ab6cb89e-d048-11ee-8370-080027b7463b'; --PID
        update nodes set exportable = true, fieldname = 'crsubstat' where nodeid = 'af750d9c-8f11-11ee-976b-080027b7463b'; --CRHP Submission Status
        update nodes set exportable = true, fieldname = 'sitename' where nodeid = 'b5cdfd32-0d05-11ed-8804-5254008afee6'; --Name
        update nodes set exportable = true, fieldname = 'datesubmit' where nodeid = 'bb294f88-8f14-11ee-aaf0-080027b7463b'; --Date Submitted to CRHP
        update nodes set exportable = true, fieldname = 'crhp_image' where nodeid = 'c27cb7c4-6d32-11ee-a6f7-080027b7463b'; --Submit to CRHP
        update nodes set exportable = true, fieldname = 'recognized' where nodeid = 'd2d91b6a-dfb3-11ed-b47a-5254004d77d3'; --Officially Recognized Site
        update nodes set exportable = true, fieldname = 'sitedoc' where nodeid = 'dc12f414-0d07-11ed-8804-5254008afee6'; --Site Document
        update nodes set exportable = true, fieldname = 'restricted' where nodeid = 'dc974e68-8f0f-11ee-85a0-080027b7463b'; --Restricted
        update nodes set exportable = true, fieldname = 'image_feat' where nodeid = 'e0f66da2-dfb2-11ed-b3d0-5254004d77d3'; --Image Features
        update nodes set exportable = true, fieldname = 'PIN' where nodeid = 'e1f9e6b6-d048-11ee-8370-080027b7463b'; --PIN
        update nodes set exportable = true, fieldname = 'datenotes' where nodeid = 'e470bafa-cdab-11ed-83b5-5254004d77d3'; --Chronology Notes
        update nodes set exportable = true, fieldname = 'borden' where nodeid = 'e5ecf044-0d06-11ed-86c8-5254008afee6'; --Borden Number
        update nodes set exportable = true, fieldname = 'imagetype' where nodeid = 'e82084a6-2fc1-11ed-8a32-5254008afee6'; --Image Type
        update nodes set exportable = true, fieldname = 'doctype' where nodeid = 'f77e8d84-37b9-11ee-95f8-080027b7463b'; --Document Type
        update nodes set exportable = true, fieldname = 'nametype' where nodeid = 'fa3a8094-0d05-11ed-8804-5254008afee6'; --Name Type
        update nodes set exportable = false, fieldname = null where nodeid = 'fdd1b2ca-cd78-11ed-b7b5-5254004d77d3'; --Construction Actors
    """


class Migration(migrations.Migration):
    dependencies = [
        ("bcrhp", "1044_disable_download_email_notifications"),
    ]

    operations = [
        migrations.RunSQL(update_config, revert_config),
    ]
