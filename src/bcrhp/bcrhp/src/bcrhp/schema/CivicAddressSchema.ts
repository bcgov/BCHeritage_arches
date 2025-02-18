import { z } from 'zod';
import {LegalDescription, LegalDescriptionSchema} from "@/bcrhp/schema/LegalDescriptionSchema.ts";
// @todo - Need to make parts of the model required if hasCivicAddress == true
const CivicAddressSchema = z.object({
    hasCivicAddress: z.boolean().default(true),
    overrideAddress: z.boolean().default(false),
    streetAddress: z.string()
        .min(1, {message: "Street Address is required."} )
        .max(80),
    city: z.string()
        .min(1, {message: "City is required."} )
        .max(80),
    province: z.string()
        .min(1, {message: "City is required."} )
        .max(80),
    postalCode: z.string()
        .max(7).refine((value:string) => /^[A-Z][0-9][A-Z] [0-9][A-Z][0-9]$/.test(value ?? ""), 'Postal Code must bie in the form "A0A A0A"'),
    locality: z.string()
        .max(50),
    locationDescription: z.string()
        .max(50),
    legalDescriptions: z.array(LegalDescriptionSchema)
});

const requiredCivicAddressSchema = CivicAddressSchema.partial({
    hasCivicAddress: true,
});

type CivicAddressType = z.infer<typeof CivicAddressSchema>;

function getCivicAddress(): CivicAddressType {
    return new CivicAddress();
}
class CivicAddress implements CivicAddressType {

    constructor() {
        this.civicAddressId = crypto.randomUUID();
        this.hasCivicAddress = true;
        this.overrideAddress = false;
        this.streetAddress = "";
        this.city = "";
        this.province = "";
        this.postalCode = "";
        this.locality = "";
        this.locationDescription = "";
        this.legalDescriptions = <LegalDescription[]>[];
    }

    civicAddressId: string;
    hasCivicAddress: boolean;
    overrideAddress: boolean;
    streetAddress: string;
    city: string;
    province: string;
    postalCode: string;
    locality: string;
    locationDescription: string;
    legalDescriptions: LegalDescription[];
}


console.log(requiredCivicAddressSchema);

export {CivicAddress, CivicAddressSchema, getCivicAddress, requiredCivicAddressSchema};
