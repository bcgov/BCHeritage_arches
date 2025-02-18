<script setup lang="ts">
import {computed, ref, provide, onMounted} from "vue";
import Stepper from 'primevue/stepper';
import Step from 'primevue/step';
import StepPanel from 'primevue/steppanel';
import StepList from 'primevue/steplist';
import StepPanels from 'primevue/steppanels';
import StepperNavigation from '@/bcgov_arches_common/components/stepper/StepperNavigation.vue';

import Panel from 'primevue/panel';

import type { Ref } from "vue";
import type { StepperProps } from "primevue/stepper";
import type { StepperState } from "primevue/stepper";

import NewSiteStep1 from "./steps/Step1_About.vue";
import SiteAddress from "./steps/Step2_SiteAddress.vue";
import SpatialLocation from "./steps/Step3_SpatialLocation.vue";
import SiteNames from "./steps/Step4_SiteNames.vue";

import {getHeritageSite} from "@/bcrhp/schema/HeritageSiteSchema.ts";
import {HeritageSite} from "@/bcrhp/schema/HeritageSiteSchema.ts";

const activateNextStep = () =>
{
  myStepper.value.d_value++;
};

const activatePreviousStep = () =>
{
  myStepper.value.d_value--;
};

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
const step3= ref();
const step4= ref();
const step5= ref();
const step6= ref();
const step7= ref();
const step8= ref();
const step9= ref();
const step10= ref();
const step11= ref();
const step12= ref();

const steps: Ref[] = [];

let lastStep = 1;
const currentStep = computed(() => {
  return myStepper.value?.d_value;
});

const stepperOptions = {
  activateCallback: activateStep
};

const submitted = ref(false);
const heritageSite: Ref<HeritageSite> = ref(getHeritageSite());

provide('heritageSite',heritageSite);

onMounted(() =>
{
  steps.push(step1, step2, step3, step4, step5, step6, step7, step8, step9, step10, step11, step12);
});

const nextLabel = computed(() => {
  if (currentStep.value === steps.length) return "Print";
  return currentStep.value < steps.length - 1 ? "Next" : "Submit";
});

const showPrevious = computed(() => {
  return !(currentStep.value === steps.length || currentStep.value === 1);
});

</script>

<template >
  <Panel header="Submit New Heritage Property" class="full-height">
    <div style="display: none">Step: {{currentStep}}</div>
    <Stepper
        ref=myStepper
        :state=stepperState
        :props=stepperProps
        :value=1
        linear
        @update:value="activateStep"
        :ptOptions=stepperOptions
    >
      <div class="bcgov-stepper">
      <div class="bcgov-vertical-steps">
        <StepList>
          <Step :value="1">Submission Information</Step>
          <Step :value="2">Site Location</Step>
          <Step :value="3">Spatial Location</Step>
          <Step :value="4">Site Names</Step>
          <Step :value="5">Official Recognition Details</Step>
          <Step :value="6">Statement of Significance</Step>
          <Step :value="7">Images</Step>
          <Step :value="8">Heritage Details</Step>
          <Step :value="9">Need Title!!</Step>
          <Step :value="10">Supporting Documents</Step>
          <Step :value="11">Review Submission</Step>
          <Step :value="12">Submission Complete</Step>
        </StepList>
      </div>
      <div class="bcgov-vertical-step-panels">
        <div class="py-6">
          <StepperNavigation
              :step-number="currentStep"
              :validate-fn="isValid"
              :show-previous="showPrevious"
              :next-label="nextLabel"
              @next-click="activateNextStep"
              @previous-click="activatePreviousStep"
          ></StepperNavigation>
        </div>
      <StepPanels>
        <StepPanel :value="1" v-slot="{ activateCallback }">
          <NewSiteStep1 ref="step1"></NewSiteStep1>
          <div class="py-6">
            <StepperNavigation
                :step-number="1"
                :show-previous="false"
                :validate-fn="isValid"
                @next-click="activateCallback(2)"
            ></StepperNavigation>
          </div>
        </StepPanel>
        <StepPanel v-slot="{ activateCallback }" :value="2" >
          <div class="flex flex-col h-48">
            <div class="step-title">Site Location</div>
          </div>
          <SiteAddress ref="step2"></SiteAddress>
          <div class="flex py-6 gap-2">
            <StepperNavigation
                :step-number="2"
                :validate-fn="isValid"
                @next-click="activateCallback(3)"
                @previous-click="activateCallback(1)"
            ></StepperNavigation>
          </div>
        </StepPanel>
        <StepPanel v-slot="{ activateCallback }" :value="3">
          <div class="flex flex-col h-48">
            <div class="step-title">Spatial Location</div>
          </div>
          <SpatialLocation ref="step3"></SpatialLocation>
          <div class="flex py-6 gap-2">
            <StepperNavigation
                :step-number="3"
                :validate-fn="isValid"
                @next-click="activateCallback(4)"
                @previous-click="activateCallback(2)"
            ></StepperNavigation>
          </div>
        </StepPanel>

        <StepPanel v-slot="{ activateCallback }" :value="4">
          <div class="flex flex-col h-48">
            <div class="step-title">Heritage Site Name(s)</div>
          </div>
          <SiteNames ref="step4"></SiteNames>
          <div class="flex py-6 gap-2">
            <StepperNavigation
                :step-number="4"
                :validate-fn="isValid"
                @next-click="activateCallback(5)"
                @previous-click="activateCallback(3)"
            ></StepperNavigation>
          </div>
        </StepPanel>

        <StepPanel v-slot="{ activateCallback }" :value="5">
          <div class="flex flex-col h-48">
            <div class="step-title">Official Recognition Details</div>
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

        <StepPanel v-slot="{ activateCallback }" :value="6">
          <div class="flex flex-col h-48">
            <div class="step-title">Statement of Significance</div>
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
        <StepPanel v-slot="{ activateCallback }" :value="7">
          <div class="flex flex-col h-48">
            <div class="step-title">Images</div>
          </div>
          <div class="py-6">
            <StepperNavigation
                :step-number="6"
                :validate-fn="isValid"
                next-label="Submit"
                @next-click="activateCallback(8)"
                @previous-click="activateCallback(6)"
            ></StepperNavigation>
          </div>
        </StepPanel>
        <StepPanel v-slot="{ activateCallback }" :value="8">
          <div class="flex flex-col h-48">
            <div class="step-title">Heritage Details</div>
          </div>
          <div class="py-6">
            <StepperNavigation
                :step-number="6"
                :validate-fn="isValid"
                next-label="Submit"
                @next-click="activateCallback(9)"
                @previous-click="activateCallback(7)"
            ></StepperNavigation>
          </div>
        </StepPanel>
        <StepPanel v-slot="{ activateCallback }" :value="9">
          <div class="flex flex-col h-48">
            <div class="step-title">Needs Title!!</div>
          </div>
          <div class="py-6">
            <StepperNavigation
                :step-number="6"
                :validate-fn="isValid"
                next-label="Submit"
                @next-click="activateCallback(10)"
                @previous-click="activateCallback(8)"
            ></StepperNavigation>
          </div>
        </StepPanel>
        <StepPanel v-slot="{ activateCallback }" :value="10">
          <div class="flex flex-col h-48">
            <div class="step-title">Supporting Documents</div>
          </div>
          <div class="py-6">
            <StepperNavigation
                :step-number="6"
                :validate-fn="isValid"
                next-label="Submit"
                @next-click="activateCallback(11)"
                @previous-click="activateCallback(9)"
            ></StepperNavigation>
          </div>
        </StepPanel>
        <StepPanel v-slot="{ activateCallback }" :value="11">
          <div class="flex flex-col h-48">
            <div class="step-title">Review Submission</div>
          </div>
          <div class="py-6">
            <StepperNavigation
                :step-number="6"
                :validate-fn="isValid"
                next-label="Submit"
                @next-click="activateCallback(12)"
                @previous-click="activateCallback(10)"
            ></StepperNavigation>
          </div>
        </StepPanel>

        <StepPanel :value="12">
          <div class="flex flex-col h-48">
            <div class="step-title">Submission Complete</div>
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
      </StepPanels>

      </div>
      </div>
    </Stepper>
  </Panel>
</template>

<style scoped>
.dashboard-card {
  font-size: 1.1rem;
  margin: 1rem;
  max-width: 33%;
}

.p-card-content {
  font-size: 1.0rem;
}
li {
  color: var(--p-primary-color)
}

.step-title {
  margin-bottom: 1rem;
  font-size: 21px;
  font-weight: bold;
  line-height: inherit;
  color: #333;
}


</style>