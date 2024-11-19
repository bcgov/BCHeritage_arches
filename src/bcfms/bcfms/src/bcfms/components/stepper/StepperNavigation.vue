<script setup lang="ts">
import Button from 'primevue/button';
import { computed } from 'vue';

const props = defineProps({
  stepNumber: {type: Number, default: 1},
  showNext: {type: Boolean, default: true},
  validateFn: {type: Function, default: null},
  nextLabel: {type: String, default: "Next"},
  validateReverse: {type: Boolean, default: false},
  showPrevious:  {type: Boolean, default: true},
  previousLabel: {type: String, default: "Previous"},
   });

const emit = defineEmits(['previousClick','nextClick']);

const proceedBlocked = computed(() => {
  return !props.validateFn ? false : !props.validateFn(props.stepNumber);
});

const reverseBlocked = computed(() => {
  return !props.validateReverse || !props.validateFn ? false : props.validateFn(props.stepNumber);
});

const clickNext = () => {
  console.log(`Trying to emit nextClick with ${props.stepNumber + 1}`);
  emit('nextClick');
  return true;
};

</script>

<template>
  <div class="stepper-nav-panel" >
    <Button
        v-if="props.showPrevious"
        :label=props.previousLabel
        :disabled="reverseBlocked"
        class="previous-button"
        severity="secondary"
        @click="$emit('previousClick', props.stepNumber-1)"
      >
    </Button>
    <Button
        v-if="props.showNext"
        :label=props.nextLabel
        :disabled="proceedBlocked"
        class="next-button"
        @click="clickNext"
    >
    </Button>
  </div>
</template>

<style scoped>
.stepper-nav-panel {
  background: var(--p-panel-background);
  display: flex;
  height: 50px;
  align-items: flex-start;
  align-self: stretch;
  margin-top: .25rem;
}

.next-button {
  position: absolute;
  right: 1rem;
}

</style>