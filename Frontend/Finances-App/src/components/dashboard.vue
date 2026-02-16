<script setup>
import api from '@/api';
import { Bar } from 'vue-chartjs';
import { ref, onMounted, computed} from 'vue';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

defineEmits(['changePage']);

const incomeData = ref([]);
const expenseData = ref([]);
const labels = ref([]);

const transactions = ref([])
const goals = ref([])

const showTrans = ref(false)
const showGoals = ref(false)


onMounted(async () => { //fetching transactions and goals
  incomeData.value  = [];
  expenseData.value = [];
  labels.value = [];
  // Fetch data if empty
  if (transactions.value.length === 0) {
    try {
    const res = await api.get('trans/');
    transactions.value = res.data;
    showTrans.value = true
    } catch(e) {
      console.log("error fetching for dashboard: ", e)
    }
  }

  if (goals.value.length === 0) {
    try {
    const res = await api.get('goal/');
    goals.value = res.data;
    showGoals.value = true
    } catch(e) {
      console.log("error fetching for dashboard: ", e)
    }
  }

  if(showTrans.value === true) {
  // last 6 only
  transactions.value.slice(-6).forEach(item => {
    // fall back to trans_date if created_on is missing
    labels.value.push(item.created_on.slice(0, 10));

    if (item.trans_type === 'Income') {
      incomeData.value.push(item.amount);
      expenseData.value.push(0); //make both arrays equal in length
    } else {
      incomeData.value.push(0);
      expenseData.value.push(item.amount);
    }
  });
}
});


const chartData = computed(() => ({
  labels: labels.value, 
  datasets: [
    {
      label: 'Income',
      backgroundColor: '#4ade80',
      data: incomeData.value.length ? incomeData.value : [0],
    },
    {
      label: 'Expenses',
      backgroundColor: '#f87171',
      data: expenseData.value.length ? expenseData.value : [0],
    },
  ],
}));

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      position: 'top',
      labels: {
        color: 'var(--color-text)', // color of "Income" and "Expenses" labels
      },
    },
    title: {
      display: true,
      text: 'Recent Income vs Expenses (Actual Date)',
      color: 'var(--color-text)', // chart title color
      font: {
        size: 16,
        weight: 'bold',
      },
    },
    tooltip: {
      bodyColor: 'var(--color-text)',     // tooltip text
      backgroundColor: 'var(--color-surface)', // tooltip background
      titleColor: 'var(--color-text)',
    },
  },
  scales: {
    x: {
      ticks: {
        color: 'var(--color-muted)', // X-axis labels
      },
      
    },
    y: {
      ticks: {
        color: 'var(--color-muted)', // Y-axis numbers
      },
    },
  },
};


</script>

<template>
<!-- Main div contains trans and goals -->
<div class="flex gap-20 ">
<!-- Transaction history box -->
 <div class="bg-primary p-6  rounded-2xl shadow-md flex-1 border h-[500px]" v-if="showTrans && transactions != ''">
      <div class="gap-2 p-4 rounded">
        <h1 class="mb-5 font-bold">Recent Transaction History</h1>
          <table class="w-full text-medium text-left border-collapse">
            <thead class="bg-primary sticky top-0 z-10">
          <tr>
            <th class="px-4 py-2">Amount</th> 
            <th class="px-4 py-2">Type</th> 
            <th class="px-4 py-2">Date</th> 
            <th class="px-4 py-2">Category</th> 
          </tr>
        </thead>
    <tbody class="divide-y divide-background">
        <tr  v-for="(item, index) in transactions.slice(-5)" :key="item.id" > 
            <td class="px-4 py-3.5" :class="item.trans_type === 'Income' ? 'text-green-600' : 'text-red-600'">{{ item.amount }}</td>
            <td class="px-4 py-3.5">{{ item.trans_type }}</td>
            <td class="px-4 py-3.5">{{ item.trans_date }}</td>
            <td class="px-4 py-3.5">{{ item.category }}</td>
          </tr>
    </tbody>
  </table>
      </div>
      <button class="mt-4 ml-4 hover:text-muted" @click="$emit('changePage', 'trans')">
        <p class="underline">View all transactions</p>
      </button>
    </div>
    <!--If no transactions are added yet-->
        <div
            class="bg-primary p-6 rounded-2xl shadow-md flex-1 border text-text h-[500px] flex flex-col"
            v-else
          >
            <!-- Top-left title -->
            <h1 class="text-black font-bold mb-6">Recent Transaction History</h1>

            <!-- Centered message -->
            <div class="flex-1 flex items-center justify-center">
              <p class="text-black text-2xl text-center">No Transactions yet. Start by adding one!</p>
            </div>
          </div>
<!--Goal Progress box-->
    <div class="bg-primary p-6 rounded-2xl shadow-md flex-1 border h-[500px] " v-if="showGoals && goals != ''" >
        <div class="gap-2 p-4 rounded">
        <h1 class="mb-5 font-bold ">Goals Progress</h1>
          <table class="w-full text-medium text-left border-collapse">
            <thead class="bg-primary sticky top-0 z-10">
          <tr>
            <th class="px-4 py-2">Target Date</th> 
            <th class="px-4 py-2">Target</th> 
            <th class="px-4 py-2">Progress</th> 
          </tr>
        </thead>
    <tbody class="divide-y divide-background">
        <tr v-for="(item, index) in goals.slice(-5)" :key="item.id" > 
            <td class="px-4 py-2" >{{ item.target_date }}</td>
            <td class="px-4 py-2">{{ item.target_amount  }}</td>
            <td class="px-4 py-2 w-40">
              <div class="w-full bg-gray-200 rounded h-4">
                <div
                  class="bg-surface h-4 rounded "
                  :style="{ width: ((item.current_amount / item.target_amount) * 100) + '%', maxWidth: 100 +'%' }"
                ></div>
              </div>
              <div class="text-xs text-black mt-1 text-center">
                {{ Math.round((item.current_amount / item.target_amount) * 100) <= 100 ? Math.round((item.current_amount / item.target_amount) * 100) : 100 }}%
              </div>
            </td>
          </tr>
    </tbody>
  </table>
      </div>
      <button class="mt-4 ml-4 hover:text-muted" @click="$emit('changePage', 'goals')">
        <p class="underline">View all goals</p>
      </button>
    </div>
    <!--If no goals are added yet-->
            <div
        class="bg-primary p-6 rounded-2xl shadow-md flex-1 border text-text flex flex-col h-[500px]"
        v-else
      >
        <!-- Top-left title -->
        <h1 class="text-black  font-bold mb-6">Goals Progress</h1>

        <!-- Centered message -->
        <div class="flex-1 flex items-center justify-center">
          <p class="text-black text-2xl text-center">No goals yet. Start by adding one!</p>
        </div>
      </div>
</div>



<!--Main div contains chart and advices-->
<div class="flex gap-20 " v-if="showTrans">
  <!-- Chart box -->
  <div class="bg-primary p-6 rounded-2xl border shadow-md flex-1 h-[500px]">
    <Bar :data="chartData" :options="chartOptions" style="height: 400px; width: 100%;" />
  </div>

  <!-- Advice box -->
  <div class="bg-primary p-6 rounded-2xl shadow-md border flex-1 h-[500px]">
    <h1 class="mb-4 text-xl font-semibold text-black">Advice</h1>
    <ul class="space-y-2 list-disc list-inside text-black">
      <li>Save a portion of every income, no matter how small.</li>
      <li>Avoid impulse purchases by waiting 24 hours before buying.</li>
      <li>Set a monthly budget and stick to it like it’s rent.</li>
    </ul>
  </div>
</div>

</template>