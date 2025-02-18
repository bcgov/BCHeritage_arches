import { z } from 'zod';
import {CivicAddress, CivicAddressSchema} from "@/bcrhp/schema/CivicAddressSchema.ts";

const HeritageSiteSchema = z.object({
    siteId: z.string().uuid(),
    bordenNumber: z.string()
        .min(1, {message: "Borden Number is required."} )
        .refine((value:string) => /^[A-Z][a-z][A-Z][a-z]-[0-9]{1-4}$/.test(value ?? ""), "Invalid Borden Number format."),
    commonName:  z.string().min(1, {message: "Common Name is required."} ) ,
    otherNames: z.array( z.string() ).max(5),
    civicAddress: z.array(CivicAddressSchema),
    siteBoundary: z.object(), // This needs to map to a GeoJSON object
    siteBoundaryIncorrect: z.boolean().default(false), // If the geometry from the PID isn't right this flags it
});

const requiredHeritageSiteSchema = HeritageSiteSchema.partial({
    commonName: true
});

type HeritageSiteType = z.infer<typeof HeritageSiteSchema>;

function getHeritageSite(): HeritageSiteType {
    return new HeritageSite();
}

// @todo - Figure out object state - New/Updated/Deleted
class HeritageSite implements HeritageSiteType {

    constructor() {
        this.siteId = crypto.randomUUID();
        this.bordenNumber = "";
        this.commonName = "";
        this.otherNames = [];
        this.hasCivicAddress = true;
        this.civicAddress = {}; // Object of UUID -> CivicAddress objects
        this.siteBoundary = {};
        this.siteBoundaryIncorrect = false;
    }
    siteId: string;
    bordenNumber: string;
    commonName: string;
    otherNames: string[];
    hasCivicAddress: boolean;
    civicAddress: object;
    siteBoundary: object;
    siteBoundaryIncorrect: boolean;
}


console.log(requiredHeritageSiteSchema);

export {HeritageSite, getHeritageSite, requiredHeritageSiteSchema};
