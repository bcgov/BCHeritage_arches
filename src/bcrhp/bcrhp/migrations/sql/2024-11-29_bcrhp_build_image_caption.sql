create or replace function bcrhp_build_image_caption(image_view text, image_features text, image_date timestamp) returns text as $$
begin
    return image_view || case when image_features is not null and image_features <> '' then ' - '||image_features else '' end ||
           case when image_date is not null then ', '||to_char(image_date,'yyyy') else '' end;
end $$
    language plpgsql;