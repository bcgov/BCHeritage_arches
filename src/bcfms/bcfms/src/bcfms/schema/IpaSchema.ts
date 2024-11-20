import { z } from 'zod';

const IpaSubmissionSchema = z.object({
    projectName: z.string().min(5).max(120),
    companyName: z.string().max(80),
    authorizingAgency: z.string().uuid(),
    projectStartDate: z.date(),
    projectEndDate: z.date(),
    projectType: z.string().uuid(),
    otherProjectType: z.string(), // Need max length
    proposedActivity: z.string(), // Need max length
    locationDescription: z.string(), // Need max length
    latitude: z.number().min(48.20).max(61.00),
    longitude: z.number().min(-139.13).max(-123.53),
    multipleGeometryQualifier: z.string() // Need max length
});

type IpaSubmissionType = z.infer<typeof IpaSubmissionSchema>;


function getIpaSubmission(): IpaSubmissionType {
    return new IpaSubmission();
}
class IpaSubmission implements IpaSubmissionType {

    constructor() {
        this.authorizingAgency = "";
        this.companyName = "";
        this.latitude = 0.00;
        this.locationDescription = "";
        this.longitude = 0.00;
        this.multipleGeometryQualifier = "";
        this.otherProjectType = "";
        this.projectEndDate = new Date();
        this.projectName = "";
        this.projectStartDate = new Date();
        this.projectType = "";
        this.proposedActivity = "";
    }

    authorizingAgency: string;
    companyName: string;
    latitude: number;
    locationDescription: string;
    longitude: number;
    multipleGeometryQualifier: string;
    otherProjectType: string;
    projectEndDate: Date;
    projectName: string;
    projectStartDate: Date;
    projectType: string;
    proposedActivity: string;
}

const requiredIpaSubmissionSchema = IpaSubmissionSchema.partial({
    projectEndDate: true,
    projectType: true,
    otherProjectType: true,
    multipleGeometryQualifier: true
});

console.log(requiredIpaSubmissionSchema);

export {IpaSubmission, getIpaSubmission, requiredIpaSubmissionSchema};
