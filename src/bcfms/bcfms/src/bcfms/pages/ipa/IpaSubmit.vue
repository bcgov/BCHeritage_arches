<script setup lang="ts">
import {computed, ref, provide, onMounted} from "vue";
import Stepper from 'primevue/stepper';
import StepItem from 'primevue/stepitem';
import Step from 'primevue/step';
import StepPanel from 'primevue/steppanel';
import StepperNavigation from '@/bcfms/components/stepper/StepperNavigation.vue';

import Panel from 'primevue/panel';

import type { Ref } from "vue";
import type { StepperProps } from "primevue/stepper";
import type { StepperState } from "primevue/stepper";
// import LabelledInput from "@/bcfms/components/labelledinput/LabelledInput.vue";

import IpaSubmitStep1 from "./steps/IpaSubmitStep1.vue";
import IpaSubmitStep2 from "./steps/IpaSubmitStep2.vue";

import {getIpaSubmission} from "@/bcfms/schema/IpaSchema.ts";
import type {IpaSubmission} from "@/bcfms/schema/IpaSchema.ts";

function activateStep(step: number) {
  if (step > lastStep && !isValid(lastStep))
  {
    myStepper.value.d_value = lastStep;
  }
  else
  {
    lastStep = step;
  }
}

const isValid = (step: number) => {
  let stepValid = true;
  if (typeof steps[step-1]?.value?.isValid === "function")
  {
    stepValid = steps[step-1]?.value?.isValid();
  }
  if (step === steps.length)
  {
    submitted.value = true;
  }
  return stepValid;
};

const printDetails = () =>
{
  console.log("printDetails");
};
const stepperProps:  Ref<StepperProps | null> = ref(null);
const stepperState:  Ref<StepperState | null> = ref(null);
const myStepper = ref();

const step1= ref();
const step2= ref();

const steps: Ref[] = [];

let lastStep = 1;
const currentStep = computed(() => {
  return myStepper.value?.d_value;
});

const stepperOptions = {
  activateCallback: activateStep
};

const submitted = ref(false);
const ipaData: Ref<IpaSubmission> = ref(getIpaSubmission());

provide('ipaData',ipaData);

onMounted(() =>
{
  steps.push(step1, step2);
});

</script>

<template >
  <Panel header="Submit New Project" class="full-height">
    <div>Step: {{currentStep}}</div>
    <Stepper
        ref=myStepper
        :state=stepperState
        :props=stepperProps
        :value=1
        linear
        @update:value="activateStep"
        :ptOptions=stepperOptions
    >
      <StepItem :value="1">
        <Step>Submission Information</Step>
        <StepPanel v-slot="{ activateCallback }">
          <IpaSubmitStep1 ref="step1"></IpaSubmitStep1>
          <div class="py-6">
            <StepperNavigation
                :step-number="1"
                :show-previous="false"
                :validate-fn="isValid"
                @next-click="activateCallback(2)"
            ></StepperNavigation>
          </div>
        </StepPanel>
      </StepItem>
      <StepItem :value="2">
        <Step>Project Details</Step>
        <StepPanel v-slot="{ activateCallback }">
          <IpaSubmitStep2 ref="step2"></IpaSubmitStep2>
          <div class="flex py-6 gap-2">
            <StepperNavigation
                :step-number="2"
                :validate-fn="isValid"
                @next-click="activateCallback(3)"
                @previous-click="activateCallback(1)"
            ></StepperNavigation>
          </div>
        </StepPanel>
      </StepItem>
      <StepItem :value="3">
        <Step>Project Type</Step>
        <StepPanel v-slot="{ activateCallback }">
          <div class="flex flex-col h-48">
            <div class="border-2 border-dashed border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 flex-auto flex justify-center items-center font-medium">
              Project Type
            </div>
          </div>
          <div class="flex py-6 gap-2">
            <StepperNavigation
                :step-number="3"
                :validate-fn="isValid"
                @next-click="activateCallback(4)"
                @previous-click="activateCallback(2)"
            ></StepperNavigation>
          </div>
        </StepPanel>
      </StepItem>

      <StepItem :value="4">
        <Step>Location</Step>
        <StepPanel v-slot="{ activateCallback }">
          <div class="flex flex-col h-48">
            <div class="border-2 border-dashed border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 flex-auto flex justify-center items-center font-medium">
              Location
            </div>
          </div>
          <div class="flex py-6 gap-2">
            <StepperNavigation
                :step-number="4"
                :validate-fn="isValid"
                @next-click="activateCallback(5)"
                @previous-click="activateCallback(3)"
            ></StepperNavigation>
          </div>
        </StepPanel>
      </StepItem>

      <StepItem :value="5">
        <Step>Documents</Step>
        <StepPanel v-slot="{ activateCallback }">
          <div class="flex flex-col h-48">
            <div class="border-2 border-dashed border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 flex-auto flex justify-center items-center font-medium">
              Documents
            </div>
          </div>
          <div class="flex py-6 gap-2">
            <StepperNavigation
                :step-number="5"
                :validate-fn="isValid"
                @next-click="activateCallback(6)"
                @previous-click="activateCallback(4)"
            ></StepperNavigation>
          </div>
        </StepPanel>
      </StepItem>

      <StepItem :value="6">
        <Step>Review Submission</Step>
        <StepPanel v-slot="{ activateCallback }">
          <div class="flex flex-col h-48">
            <div class="border-2 border-dashed border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 flex-auto flex justify-center items-center font-medium">Content III</div>
          </div>
          <div class="py-6">
            <StepperNavigation
                :step-number="6"
                :validate-fn="isValid"
                next-label="Submit"
                @next-click="activateCallback(7)"
                @previous-click="activateCallback(5)"
            ></StepperNavigation>
          </div>
        </StepPanel>
      </StepItem>
      <StepItem :value="7">
        <Step>Submission Complete</Step>
        <StepPanel>
          <div class="flex flex-col h-48">
            <div class="border-2 border-dashed border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 flex-auto flex justify-center items-center font-medium">Content III</div>
          </div>
          <div class="py-6">
            <StepperNavigation
                :step-number="7"
                :validate-fn="isValid"
                :show-previous="false"
                next-label="Print"
                @next-click="printDetails"
            ></StepperNavigation>
          </div>
        </StepPanel>
      </StepItem>
    </Stepper>
  </Panel>
</template>

<style scoped>
.dashboard-card {
  font-size: 1.1rem;
  margin: 1rem;
  max-width: 33%;
}

.dashboard-card.ipa {
  background: rgba(215, 48, 39, 0.7);
  color: #000;
}

.p-card-content {
  font-size: 1.0rem;
}
li {
  color: var(--p-primary-color)
}

</style>