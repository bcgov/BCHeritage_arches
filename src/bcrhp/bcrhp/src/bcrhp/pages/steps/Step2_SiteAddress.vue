<script setup lang="ts">
import {useTemplateRef, inject, ref, onMounted} from "vue";
import type { Ref } from "vue";

import FieldSet from 'primevue/fieldset';
import InputText from 'primevue/inputtext';
import Checkbox from 'primevue/checkbox';
import Button from 'primevue/button';

import LabelledInput from "@/bcgov_arches_common/components/labelledinput/LabelledInput.vue";
import LabelledCheckboxInput from "@/bcgov_arches_common/components/labelledinput/LabelledCheckbox.vue";
import type {HeritageSite} from "@/bcrhp/schema/HeritageSiteSchema.ts";
import type { CivicAddress } from "@/bcrhp/schema/CivicAddressSchema.ts";
import { getCivicAddress } from "@/bcrhp/schema/CivicAddressSchema.ts";
import { requiredCivicAddressSchema } from "@/bcrhp/schema/CivicAddressSchema.ts";
import type { ZodError } from "zod";
import {fetchConcepts} from "@/bcrhp/api.ts";


const heritageSite: HeritageSite = inject('heritageSite') as HeritageSite;
// const civicAddress: { [id: string] : CivicAddress; } = heritageSite.value.civicAddress;
let currentCivicAddress: CivicAddress = getCivicAddress();
// civicAddress[currentCivicAddress.civicAddressId] = currentCivicAddress;

// This is needed to access the IPA Data in methods? The above appears to be undefined after mounting.
const civicAddressRef: Ref<CivicAddress> = ref(currentCivicAddress);

type FormErrors = Partial<Record<keyof CivicAddress, string[]>>;
const errors: Ref<FormErrors> = ref<FormErrors>({});

const concepts = ref([]);

// These names need to match the Zog schema
const fields = {
  streetAddressField: useTemplateRef("streetAddressField"),
  cityField: useTemplateRef("cityField"),
  postalCodeField: useTemplateRef("postalCodeField"),
  locationDescriptionField: useTemplateRef("locationDescriptionField"),
  localityField: useTemplateRef("localityField"),
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

const valueUpdated = function(value: string | undefined) {
  console.log(`valueUpdated: ${value}`);
};

const valueChanged = function(event: Event) {
  console.log(`valueChanged`);
  validateField(event.target as HTMLInputElement);
};

const onFocusHandler = function(event: Event) {
  console.log(`onFocusHandler ${event}`);
  // (event.target as HTMLInputElement).classList.remove("p-invalid");
};

const onFocusOutHandler = function(event: Event) {
  console.log(`onFocusOutHandler`);
  validateField(event.target as HTMLInputElement);
  // (event.target as HTMLInputElement).classList.remove("p-invalid");
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

const saveAddress = function()
{
  console.log("Save address");
  heritageSite.value.civicAddress[currentCivicAddress.civicAddressId] = currentCivicAddress;
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

fetchConcepts("6021f510-ec29-4cd5-a7c4-e971ac7d9cf8", concepts);
onMounted(() => {
});

</script>
<template>
  <div class="flex flex-col h-48">
    <div style="display: none;">Child {{currentCivicAddress}}</div>
    <div class="border-2 border-dashed border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 flex-auto flex justify-center items-center font-medium">
        <LabelledCheckboxInput
            label="This site does not have a Street Address"
            hint="Check if the site doesn't have a Street Address"
            input-name="hasCivicAddress">
          <Checkbox
              id="hasCivicAddress"
              ref="hasCivicAddress"
              :model-value="!currentCivicAddress.hasCivicAddress"
              aria-describedby="has-civic-address-help"
              aria-required="true"
              fluid
              binary
              small
              @change="hasAddressChanged"
          />
      </LabelledCheckboxInput>
      <FieldSet
          id="civicAddressFieldset"
          legend="Civic Address"
          :disabled="disableAddressSection"
      >
        <LabelledInput
            label="Street Address"
            hint="Select the government with the jurisdiction over the site"
            input-name="authorizingAgency"
            :error-message="errors.streetAddress?.join(',')"
            :required="true">
          <div class="p-inputtext-fluid">
          <InputText
              id="streetAddress"
              ref="streetAddressField"
              v-model="currentCivicAddress.streetAddress"
              aria-describedby="username-help"
              aria-required="true"
              fluid
              class="inline-block"
              @change="valueChanged"
              @focus="onFocusHandler"
              @focusout="onFocusOutHandler"
              @update:model-value="valueUpdated"
          />
          <Button
              id="validateAddress"
              label="Validate"
              class="inline-block"
          ></Button>
          </div>
        </LabelledInput>
        <LabelledInput
            label="City"
            hint="Enter a unique name for your project."
            input-name="city"
            :error-message="errors.city?.join(',')"
            :required="true">
          <InputText
              id="city"
              ref="cityField"
              v-model="currentCivicAddress.city"
              aria-describedby="city-help"
              aria-required="true"
              fluid
              @change="valueChanged"
              @focus="onFocusHandler"
              @focusout="onFocusOutHandler"
              @update:modelValue="valueUpdated"
          />
          <!--              @value-change="valueUpdated"-->
        </LabelledInput>
        <LabelledInput
            label="Postal Code"
            hint="Enter address postal code"
            input-name="postalCode"
            :error-message="errors.postalCode?.join(',')"
            :required="true">
          <InputText
              id="postalCode"
              ref="postalCodeField"
              v-model="currentCivicAddress.postalCode"
              aria-describedby="postal-code-help"
              fluid
              @change="valueChanged"
              @focus="onFocusHandler"
              @focusout="onFocusOutHandler"
              @update:modelValue="valueUpdated"
          />
        </LabelledInput>
        <LabelledInput
            label="Location Description"
            hint="Location description of the site if there is no street address"
            input-name="locationDescription"
            :error-message="errors.locationDescription?.join(',')"
            :required="true">
          <InputText
              id="locationDescription"
              ref="locationDescriptionField"
              v-model="currentCivicAddress.locationDescription"
              aria-describedby="postal-code-help"
              fluid
              @change="valueChanged"
              @focus="onFocusHandler"
              @focusout="onFocusOutHandler"
              @update:modelValue="valueUpdated"
          />
        </LabelledInput>
        <LabelledInput
            label="Locality (Optional)"
            hint="Established area or neighbourhood the site is located within"
            input-name="locality"
            :error-message="errors.locality?.join(',')">
          <InputText
              id="locality"
              ref="localityField"
              placeholder="Enter the Locality"
              v-model="currentCivicAddress.locality"
              aria-describedby="locality-help"
              fluid
              @change="valueChanged"
              @focus="onFocusHandler"
              @focusout="onFocusOutHandler"
              @update:modelValue="valueUpdated"
          />
        </LabelledInput>
        <Button
            label="Add Address"
            @click="saveAddress"
          />
      </FieldSet>
      </div>
    </div>
</template>

<style>
 .inline-block {
   display: inline-block;
   width: unset;
 }
</style>