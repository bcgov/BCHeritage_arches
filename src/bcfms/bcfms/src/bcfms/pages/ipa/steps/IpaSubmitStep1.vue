<script setup lang="ts">

const isValid = () => {
  return true;
};

// This needs to be removed - added becuse ESLint was complaining. Need to figure out
// configuration so API methods are not
isValid();
defineExpose(["isValid"]) ;

</script>
<template>
          <div class="flex flex-col h-48">
            <div class="border-2 border-dashed border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 flex-auto flex justify-center items-center font-medium">
              <div>Before you begin</div>
              <div>The entire submission will need to be completed at once.</div>

              <div>You will need the following:

              <ol>
                <li>First thing</li>
                <li>Second thing</li>
                <li>Third thing</li>
              </ol>
              </div>
              <div>...
                ..</div>

              <div>When you are ready to proceed press the start button to start the submission.</div>

              Question? Contact....
            </div>
          </div>
</template>
