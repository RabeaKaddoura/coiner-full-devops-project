<script setup>//including setup in the script tag is shorter and cleaner. It also includes export default and other important functions.
import { ref } from 'vue';
import NavBar from '@/components/NavBar.vue';
import SideBar from '@/components/SideBar.vue';
import TopPanel from '@/components/TopPanel.vue';
import DataTable from '@/components/DataTable.vue';
import Dashboard from '@/components/dashboard.vue';
import Reports from '@/components/Reports.vue';



const budgHeaders =ref(["Amount","Budget Date","Category", "Description"]) 
const tranTableHeaders =ref(["Amount","Transaction Type","Wallet", "Transaction Date", "Category", "Description"]) 
const goalTableHeaders =ref(["Current Amount","Start date","Category", "Target Amount", "Target Date", "Description", "Progress"]) 
const currentPage = ref('dash') 

const changePage = (page) => { //controls the rendering of a table by passing the table's name, which is then used in the SideBar component
  currentPage.value = page
}

</script>

<template>
  <div class="flex flex-col h-screen bg-background">
    <!-- Top navigation bar -->
    <NavBar />
    
    <!-- Main layout: sidebar and main content -->
    <div class="flex bg-background">
      <!-- Sidebar -->
      <SideBar @changePage="changePage"/>

      <!-- Main content area: top panel and data table -->
      <div class="flex flex-col flex-1 p-13 space-y-10 ">
        <TopPanel :key="'top-' + currentPage"/> <!--a key of current page is added here so that whenever it changes the components re-mount to display latest wallet values-->
        <Dashboard v-if="currentPage==='dash'" @changePage="changePage"/>
        <Reports v-if="currentPage==='reports'" :key="'reports-' + currentPage"/>
        <DataTable v-if="currentPage==='trans'" title="Transactions" subtitle="Add Transactions To The Record" :headersArr="tranTableHeaders" :isTransTable="true" :key="'trans-' + currentPage"/>
        <DataTable v-if="currentPage==='budget'" title="Budget" subtitle="Add Budgets To The Record" :headersArr="budgHeaders" :isBudgetTable="true" :key="'budget-' + currentPage"/>
        <DataTable v-if="currentPage==='goals'" title="Goals" subtitle="Add Goals To the Record" :headersArr="goalTableHeaders" :isGoalsTable="true" :key="'goals-' + currentPage"/>
      </div>
    </div>
     <!--Footer-->
      <footer class="bg-surface text-text border border-border">
        <div class="max-w-7xl mx-auto px-4 py-6 flex flex-col sm:flex-row justify-between items-center">
          <p class="text-sm">&copy; {{ new Date().getFullYear() }} Coiner. All rights reserved.</p>
          <div class="flex space-x-2 mt-2 sm:mt-0 text-sm">
            <h1>Contact Email:</h1>
            <p>rabea3.kadd@hotmail.com</p>
          </div>
        </div>
    </footer>
  </div>
</template>
