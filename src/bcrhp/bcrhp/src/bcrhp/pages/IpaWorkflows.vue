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
    label: $gettext("Submit IPA"),
    description: $gettext("Create a new IPA"),
    icon: "fa fa-file",
    class: "dashboard-card ipa",
    routeName: routeNames.ipaSubmit
  },

]);
</script>
<template>
  <Panel header="Industry Project Assessment (IPA) Filings" class="full-height">
    <Fluid style="flex-direction: column">
      <div class="grid grid-cols-3 gap-4" style="display:flex; gap: 1rem;">
      <Card
          v-for="item in workflowItems" :key="item.routeName"
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