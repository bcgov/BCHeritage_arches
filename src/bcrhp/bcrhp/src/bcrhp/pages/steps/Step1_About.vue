<script setup lang="ts">

const isValid = () => {
  return true;
};

defineExpose({isValid});

</script>
<template>
  <div class="flex flex-col h-48">
    <div
        class="border-2 border-dashed border-surface-200 dark:border-surface-700 rounded bg-surface-50 dark:bg-surface-950 flex-auto flex justify-center items-center font-medium">

      <div class="about-section">
        <div class="about-title">Before you begin</div>

        <div>Confirm the site does not already exist on the BC Register of Historic Places by doing the following
          searches on the Search Page. Consult the <a href="">How to Search PDF Guide</a> as needed.
        </div>

        <ul>
          <li>
            Keyword search in the Find a resource... search bar
          </li>
          <li>
            Address search in the map Find an address... search bar
          </li>
          <li>
            Zoom into map location and verify there is no site
          </li>
        </ul>
      </div>

      <div class="about-title">
        Submission Requirements
      </div>


      <div class="about-section">
      <ul>
        <li>
          Steps 1-5 are mandatory to complete the basic data requirements for a notification.
        </li>
        <li>
          Required documents for Step 11 include:
          <ol>
            <li>
              Covering notification letter
            </li>
            <li>
              Copy of Bylaw, Resolution, or Meeting Minutes
            </li>
            <li>
              GIS files or Site Map
            </li>
          </ol>
        </li>
        </ul>

        <div>
          See the Heritage Property Notifications Guide for more information including Canadian Register Nomination
          Requirements. It is highly recommended to complete the remaining steps if information is available to improve
          the historic site’s search ability on the register.
        </div>

        <div>When you are ready to proceed press the start button to begin the submission.</div>
        </div>

    </div>
  </div>
</template>

<style>
.about-title {
  display: block;
  width: 100%;
  padding: 0;
  margin-bottom: .5rem;
  font-size: 21px;
  font-weight: bold;
  line-height: inherit;
  color:#333;
}

.about-section {
  margin-bottom: 1rem;
}

li {
  color: unset;
  font-size: unset;
}
</style>
