<script setup lang="ts">
import {useTemplateRef, inject, ref, onMounted} from "vue";
import type { Ref } from "vue";

import FieldSet from 'primevue/fieldset';
import Checkbox from 'primevue/checkbox';

import LabelledInput from "@/bcgov_arches_common/components/labelledinput/LabelledInput.vue";
import LabelledCheckboxInput from "@/bcgov_arches_common/components/labelledinput/LabelledCheckbox.vue";
import type {HeritageSite} from "@/bcrhp/schema/HeritageSiteSchema.ts";
import type { CivicAddress } from "@/bcrhp/schema/CivicAddressSchema.ts";
import { getCivicAddress } from "@/bcrhp/schema/CivicAddressSchema.ts";
import { requiredCivicAddressSchema } from "@/bcrhp/schema/CivicAddressSchema.ts";
import type { ZodError } from "zod";


const heritageSite: HeritageSite = inject('heritageSite') as HeritageSite;
// const civicAddress: { [id: string] : CivicAddress; } = heritageSite.value.civicAddress;
let currentCivicAddress: CivicAddress = getCivicAddress();
// civicAddress[currentCivicAddress.civicAddressId] = currentCivicAddress;

// This is needed to access the IPA Data in methods? The above appears to be undefined after mounting.
const civicAddressRef: Ref<CivicAddress> = ref(currentCivicAddress);

type FormErrors = Partial<Record<keyof CivicAddress, string[]>>;
const errors: Ref<FormErrors> = ref<FormErrors>({});

// These names need to match the Zog schema
const fields = {
};

const isValid = () => {
  // We don't want to validate fields the first time we show the step
  if (!validateFields)
  {
    validateFields = true;
    return true;
  }
  if (!currentCivicAddress.hasCivicAddress)
  {
    return true;
  }
  let valid = true;

  for (const field of Object.values(fields) as Array<Ref>) {
    valid = validateField(field?.value.$el as HTMLInputElement) && valid;
  }
  return valid;
};

const validateField = function(field: HTMLInputElement) {
  console.log(`ID: ${field.id}`);
  const key: keyof CivicAddress = field.id as keyof CivicAddress;
  const fieldValidation = requiredCivicAddressSchema.shape[key].safeParse(civicAddressRef.value[key]);
  if (fieldValidation.success)
  {
    field.classList.remove("p-invalid");
    errors.value[key] = [];
  }
  else
  {
    field.classList.add("p-invalid");
    errors.value[key] = (fieldValidation.error as ZodError).flatten().formErrors;
  }
  return fieldValidation.success;
};

const disableAddressSection = ref(false);

const hasAddressChanged = function () {
  currentCivicAddress.hasCivicAddress = !currentCivicAddress.hasCivicAddress;
  console.log(`Has address?: ${currentCivicAddress.hasCivicAddress}`);
  disableAddressSection.value = !currentCivicAddress.hasCivicAddress;
};


let validateFields = false;


// This needs to be removed - added because ESLint was complaining. Need to figure out
// configuration so API methods are not
defineExpose({isValid}) ;

onMounted(() => {
});

</script>
<template>
  <div class="flex flex-col h-48">
    <div style="display: none;">Child {{currentCivicAddress}}</div>
    <div class="border-2 border-dashed border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 flex-auto flex justify-center items-center font-medium">
      <FieldSet
          id="siteBoundaryFieldSet"
          legend="Site Boundary"
          style="width: 45%; display: inline-block"
      >
        <LabelledCheckboxInput
            label="Site Boundary icorrect"
            hint="Update the geometry"
            input-name="hasCivicAddress">
          <Checkbox
              id="boundaryIncorrect"
              ref="boundaryIncorrectField"
              :model-value="heritageSite.siteBoundaryIncorrect"
              aria-describedby="has-civic-address-help"
              aria-required="true"
              fluid
              binary
              small
              @change="hasAddressChanged"
          />
        </LabelledCheckboxInput>
        <LabelledInput
            label="Site Boundary"
            hint="Drag KML, GeoJSON or Shapefile here"
            input-name="authorizingAgency"
            :error-message="errors.streetAddress?.join(',')"
            :required="true">
          <div>
            Need geometry upload component for Geometry upload
          </div>
          <div>
            Need map display component
          </div>
          <div class="instructions">
            <div>
              If there is no geospatial data/file add a Site Map under the Supporting Documents step.
            </div>
            <div>
              If the geospatial file does not import successfully, add files under the Supporting Documents step.
            </div>
          </div>
        </LabelledInput>
      </FieldSet>
      <div style="width: 45%; display: inline-block; background-color: darkgoldenrod; height: 400px"></div>
      </div>
    </div>
</template>

<style>
 .inline-block {
   display: inline-block;
   width: unset;
 }
</style>