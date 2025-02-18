<script setup lang="ts">
import { ref } from "vue";
import Card from 'primevue/card';
import Panel from 'primevue/panel';
import Fluid from 'primevue/fluid';
import { useGettext } from "vue3-gettext";

import { routeNames } from "@/bcrhp/routes.ts";

const { $gettext } = useGettext();
const workflowItems = ref([
  {
    label: $gettext("Submit a new site"),
    description: $gettext("Submit a site that is not on the register"),
    icon: "fa fa-file",
    class: "dashboard-card ipa",
    routeName: routeNames.newSite
  },
  {
    label: $gettext("Update an existing site"),
    description: $gettext("Submit updates to an existing site on the register"),
    icon: "fa fa-file",
    class: "dashboard-card collection-event",
    routeName: routeNames.updateSite
  },
]);
</script>
<template>
  <Panel header="Workflows" class="full-height">
    <Fluid style="flex-direction: column">
    <div class="grid grid-cols-3 gap-4" style="display:flex; gap: 1rem;">
        <Card
            v-for="item in workflowItems"
            :key="item.routeName"
            :class="item.class">
        <template #title>
          <router-link
                  :to="{name: item.routeName}"
                  class="dashboard-card-link"
          >
            {{ item.label }}
          </router-link>
          </template>
        <template #content>
          <p class="m-0">
            {{ item.description }}
          </p>
        </template>
          </Card>
      </div>
    </Fluid>
  </Panel>
</template>

<style scoped>


</style>

<style>
.dashboard-card {
  /*margin: 1rem;*/
  min-width: 33%;
  /*display: inline-block;*/
}

.dashboard-card.ipa {
  border: solid thick rgba(53,151,143,0.7);
}

.dashboard-card.collection-event {
  border: solid thick rgba(50,50,50,0.7);
}

</style>