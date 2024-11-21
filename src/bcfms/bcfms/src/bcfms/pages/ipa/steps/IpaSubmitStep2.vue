<script setup lang="ts">
import {inject, ref, onMounted} from "vue";
import type { Ref } from "vue";

import FieldSet from 'primevue/fieldset';
import InputText from 'primevue/inputtext';
import Select from 'primevue/select';

import LabelledInput from "@/bcfms/components/labelledinput/LabelledInput.vue";
import type {IpaSubmission} from "@/bcfms/schema/IpaSchema.ts";
import {requiredIpaSubmissionSchema} from "@/bcfms/schema/IpaSchema.ts";
import {ZodError} from "zod";
import {fetchConcepts} from "@/bcfms/api.ts";


const childIpaData: IpaSubmission = inject('ipaData') as IpaSubmission;

type FormErrors = Partial<Record<keyof IpaSubmission, string[]>>;
const errors: Ref<FormErrors> = ref<FormErrors>({});

const concepts = ref([]);
// These names need to match the Zog schema
const fields = {
  projectName: ref(),
  companyName: ref(),
  authorizingAgency: ref()
};

const isValid = () => {
  let valid = true;
  let result;
  Object.keys(fields).forEach(fieldName => {
    result = requiredIpaSubmissionSchema.shape[fieldName as keyof IpaSubmission]
        .safeParse(childIpaData[fieldName as keyof IpaSubmission]);
    valid = valid && result.success;
  });
  return valid;
};

const valueUpdated = function($event: Event, value: string) {
  console.log(`valueUpdated: ${$event}: ${value}`);
};

const valueChanged = function(event: Event) {
  console.log(`valueChanged`);
  validateField(event);
};

const onFocusHandler = function(event: Event) {
  console.log(`onFocusHandler ${event}`);
  // (event.target as HTMLInputElement).classList.remove("p-invalid");
};

const onFocusOutHandler = function(event: Event) {
  console.log(`onFocusOutHandler`);
  validateField(event);
  // (event.target as HTMLInputElement).classList.remove("p-invalid");
};

const validateField = function(event: Event) {
  console.log(`validateField: ${event}`);
  const target = event.target as HTMLInputElement;
  const key: keyof IpaSubmission = target.id as keyof IpaSubmission;
  const fieldValidation = requiredIpaSubmissionSchema.shape[key].safeParse(target.value);
  if (fieldValidation.success)
  {
    target.classList.remove("p-invalid");
    errors.value[key] = [];
  }
  else
  {
    target.classList.add("p-invalid");
    errors.value[key] = (fieldValidation.error as ZodError).flatten().formErrors;
  }
};

const projectName = ref();
const companyName = ref();
const authorizingAgency = ref();

// This needs to be removed - added because ESLint was complaining. Need to figure out
// configuration so API methods are not
defineExpose({isValid}) ;

fetchConcepts("6021f510-ec29-4cd5-a7c4-e971ac7d9cf8", concepts);
onMounted(() => {
  fields.projectName = projectName;
  fields.companyName = companyName;
  fields.authorizingAgency = authorizingAgency;
});

</script>
<template>
  <div class="flex flex-col h-48">
    <div>Child {{childIpaData.projectName}}</div>
    <div class="border-2 border-dashed border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 flex-auto flex justify-center items-center font-medium">
      <FieldSet legend="Details">
        <LabelledInput
            label="Project Name"
            hint="Enter a unique name for your project."
            input-name="projectName"
            :error-message="errors.projectName?.join(',')"
            :required="true">
          <InputText
              id="projectName"
              ref="projectName"
              v-model="childIpaData.projectName"
              aria-describedby="username-help"
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
            label="Industry Company / Individual / Organization"
            hint="Enter the name of the Company / Individual / Organization that is responsible for executing the project."
            input-name="companyName"
            :error-message="errors.companyName?.join(',')"
            :required="true">
          <InputText
              id="companyName"
              ref="companyName"
              v-model="childIpaData.companyName"
              aria-describedby="companyname-help"
              aria-required="true"
              fluid
              @change="valueChanged"
              @focus="onFocusHandler"
              @focusout="onFocusOutHandler"
          />
        </LabelledInput>
        <LabelledInput
            label="Authorizing Agency"
            hint="Select the Agency that is authorizing the project."
            input-name="authorizingAgency"
            :error-message="errors.authorizingAgency?.join(',')"
            :required="true">
          <Select
              id="authorizingAgency"
              ref="authorizingAgency"
              :options="concepts"
              option-value="conceptid"
              option-label="text"
              placeholder="Select Agency"
              v-model="childIpaData.authorizingAgency"
              aria-describedby="authorizing-agency-help"
              aria-required="true"
              fluid
          />
        </LabelledInput>
      </FieldSet>
    </div>
  </div>
</template>
