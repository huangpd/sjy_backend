<template>
  <el-container>
    <!-- <el-header>Header</el-header> -->

    <el-main>
      <el-row id="TownHome" style="display: flow-root" type="flex" justify="start" :gutter="10">
        <el-col :span="8">
          <el-row>
            <el-col :span="4">
              <el-button-group>
                <el-button type="primary" icon="el-icon-edit">地区选择</el-button>
              </el-button-group>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="4">
              <el-button-group>
                <el-cascader size="large" :options="options" v-model="area" @change="handleChange"></el-cascader>
              </el-button-group>
            </el-col>
          </el-row>

          <el-row>
            <el-button-group>
              <el-button type="primary" icon="el-icon-edit">累计入驻公司 注册资本综合</el-button>
            </el-button-group>

            <el-card class="box-card font_s" v-if="this.endVal">
              <countTo :startVal="startVal" v-bind:endVal="this.endVal" :duration="5000"></countTo>万元
            </el-card>
          </el-row>

          <el-row>
            <el-col :span="6">
              <el-button-group>
                <el-button
                  type="primary"
                  icon="el-icon-edit"
                  @click="sssss"
                >累计注册公司：{{company_amount}} 家</el-button>
              </el-button-group>
              <div style="width:400px">
                <ve-pie :data="chartData2"></ve-pie>
              </div>
            </el-col>
          </el-row>
        </el-col>

        <el-col :span="16">
          <ve-histogram
            :data="chartData1"
            :data-zoom="dataZoom1"
            :settings="chartSettings1"
            :loading="loading"
            height="800px"
          ></ve-histogram>
        </el-col>
      </el-row>

      <el-row>
        <el-collapse v-model="activeNames" @change="handleChange">
          <el-collapse-item title="全国私募分布图" name="1">
            <el-col :span="24">
              <el-button-group>
                <el-button type="primary" icon="el-icon-edit">私募公司分布</el-button>
              </el-button-group>
              <span>当前选中了: {{ cityName || '-' }}</span>
              <ve-map
                :data="chartData8"
                :settings="chartSettings8"
                :events="chartEvents8"
                height="800px"
                width="100vh"
              ></ve-map>
            </el-col>
          </el-collapse-item>
        </el-collapse>
      </el-row>

      <el-divider content-position="center">私募基金小镇系统</el-divider>

      <el-row>
        <el-button-group>
          <el-button type="primary" icon="el-icon-edit">入驻私募公司风险揭示</el-button>
        </el-button-group>
        <br>
        <template>
          <el-table :data="company_risk" border height="20vh" style="width: 100%" stripe>
            <el-table-column prop="company_name" label="公司名" width="120"></el-table-column>

            <el-table-column prop="company_search_shi_xin" label="失信被执行人信息" width="150">
              <template slot-scope="scope">
                <div slot="reference" class="name-wrapper">
                  <el-tag size="medium">共 {{ scope.row.company_search_shiXin_amount }} 条</el-tag>
                </div>
              </template>
            </el-table-column>

            <el-table-column prop="company_search_court_notice" label="查询开庭公告" width="120">
              <template slot-scope="scope">
                <div slot="reference" class="name-wrapper">
                  <el-tag size="medium">共 {{ scope.row.company_court_notice_amount }} 条</el-tag>
                </div>
              </template>
            </el-table-column>

            <el-table-column prop="company_get_op_exception" label="企业经营异常信息" width="150">
              <template slot-scope="scope">
                <div slot="reference" class="name-wrapper">
                  <el-tag size="medium">共 {{ scope.row.company_abnormal_amount }} 条</el-tag>
                </div>
              </template>
            </el-table-column>

            <el-table-column fixed="right" label="操作" width="100">
              <template slot-scope="scope">
                <el-button @click="handleClick(scope.row)" type="text" size="small">查看详情</el-button>
              </template>
            </el-table-column>
          </el-table>
        </template>
      </el-row>

      <el-row>
        <el-col :span="24"></el-col>

        <el-col :span="7">
          <el-col :span="24">
            <el-button-group>
              <el-button type="primary" icon="el-icon-edit">数据统计</el-button>
            </el-button-group>

            <el-col :span="24">
              <el-card shadow="hover">
                已入驻公司
                <h3>{{ this.multiCompany_amount }}</h3>
              </el-card>

              <el-card shadow="hover">
                私募管理人
                <h3>{{ this.multiManager_amount }}</h3>
              </el-card>

              <el-card shadow="hover">
                私募产品
                <h3>{{ this.multiProduct_amount }}</h3>
              </el-card>
              <el-card shadow="hover">
                入驻资金规模
                <h3>{{ this.multiCapital_size }}</h3>
              </el-card>
            </el-col>
          </el-col>
        </el-col>

        <el-col :span="1" class="shensk">
          <el-divider direction="vertical"></el-divider>
        </el-col>

        <el-col :span="7">
          <el-col :span="24">
            <el-button-group>
              <el-button type="primary" icon="el-icon-edit">企业占比</el-button>
            </el-button-group>
            <ve-pie :data="chartData3" width="20vw"></ve-pie>
          </el-col>
        </el-col>

        <el-col :span="1" class="shensk">
          <el-divider direction="vertical"></el-divider>
        </el-col>

        <el-col :span="7">
          <el-col :span="24">
            <el-button-group>
              <el-button type="primary" icon="el-icon-edit">管理人类型</el-button>
            </el-button-group>
            <ve-pie :data="chartData6" :settings="chartSettings6" width="20vw"></ve-pie>
          </el-col>
        </el-col>

        <el-col :span="24">
          <el-divider content-position="center">私募基金小镇系统</el-divider>
        </el-col>
      </el-row>
    </el-main>

    <el-footer></el-footer>
  </el-container>
</template>

<script>
import { regionDataPlus, CodeToText } from "element-china-area-data";
import countTo from "vue-count-to";
import http from "@/utils/http";
import api from "@/utils/api";

export default {
  name: "TownHome",
  components: { countTo },
  data() {
    return {
      enterCapital_size: 0,

      multiCompany_amount: 0,
      multiManager_amount: 0,
      multiProduct_amount: 0,
      multiCapital_size: 0,

      startVal: 0,
      endVal: 0,
      date_min: 2018,
      date_max: 2019,
      options: regionDataPlus,
      area: [],
      loading: true,
      options1: [
        {
          value: "选项1",
          label: "浙江"
        },
        {
          value: "选项2",
          label: "上海"
        }
      ],
      options2: [
        {
          value: "选项1",
          label: "城市1"
        },
        {
          value: "选项2",
          label: "城市2"
        }
      ],
      options3: [
        {
          value: "选项1",
          label: "小镇1"
        },
        {
          value: "选项2",
          label: "小镇2"
        }
      ],

      chartData1: {
        columns: ["日期", "有限合伙", "有限责任", "总量"],
        rows: []
      },
      dataZoom1: {
        type: "slider",
        start: 0,
        end: 100
      },
      chartSettings1: {
        showLine: ["总量"]
      },
      dataEmpty1: true,
      company_amount: 0,

      company_risk: [
        {
          company_abnormal_amount: 0,
          company_court_notice_amount: 0,
          company_name: "",
          company_search_shiXin_amount: 0,
          company_uid: " ",
          uid: ""
        }
      ],

      chartData2: {
        columns: ["日期", "访问用户"],
        rows: [
          { 日期: "其他", 访问用户: 23 },
          { 日期: "有限合伙", 访问用户: 230 },
          { 日期: "有限责任", 访问用户: 564 }
        ]
      },
      chartData3: {},
      chartData6: {
        columns: ["日期", "访问用户"],
        rows: [
          { 日期: "私募产品", 访问用户: 10 },
          { 日期: "私募管理人", 访问用户: 21 }
        ]
      },
      chartSettings6: {
        roseType: "radius"
      },
      chartData8: {
        columns: ["位置", "私募公司数量"],
        rows: []
      },
      chartSettings8: {
        position: "china",
        // selectData: true,
        selectedMode: "single"
      },
      cityName: "",
      chartEvents8: {
        click: v => {
          this.cityName = v.name;
        }
      },
      companys: 817
    };
  },

  methods: {
    handleChange(value) {
      var province = CodeToText[value[0]];
      var city = CodeToText[value[1]];
      var area = CodeToText[value[2]];

      console.log(value);
      console.log(province, city, area);

      if (!province || province == "全部") {
        province = "None";
      }
      if (!city || city == "全部") {
        city = "None";
      }
      if (!area || area == "全部") {
        area = "None";
      }

      this.company_message_date_v(province, city, area);
    },
    handleChange_delete() {
      this.selectedOptions = [];
    },
    company_message_date: async function() {
      let params = {
        date_min: this.date_min,
        date_max: this.date_max,
        province: "",
        city: "",
        area: ""
      };
      const res = await http.post(api.company_message_date, params);
      if (res.data.value == 1) {
        this.chartData1.rows = res.data.message;
        if (this.chartData1.rows.length !== 0) {
          this.loading = false;
        }
        this.company_amount = res.data.amount;
        this.endVal = res.data.enterCapital_size;
        var sum_amount = res.data.sum_amount;
        var part_amount = res.data.part_amount;
        var duty_amount = res.data.duty_amount;
        var oter_amount = sum_amount - part_amount - duty_amount;
        this.chartData2 = {
          columns: ["日期", "访问用户"],
          rows: [
            { 日期: "其他", 访问用户: oter_amount },
            { 日期: "有限合伙", 访问用户: part_amount },
            { 日期: "有限责任", 访问用户: duty_amount }
          ]
        };
      }
    },
    company_message_date_v: async function(province, city, area) {
      let params = {
        date_min: this.date_min,
        date_max: this.date_max,
        province: province,
        city: city,
        area: area
      };
      const res = await http.post(api.company_message_date, params);
      if (res.data.value == 1) {
        this.chartData1.rows = res.data.message;
        this.enterCapital_size = res.data.enterCapital_size;
        if (this.chartData1.rows.length !== 0) {
          this.dataEmpty1 = false;
        } else {
          this.dataEmpty1 = true;
        }
        this.company_amount = res.data.amount;
        this.company_amount = res.data.amount;
        this.endVal = res.data.enterCapital_size;
        var sum_amount = res.data.sum_amount;
        var part_amount = res.data.part_amount;
        var duty_amount = res.data.duty_amount;
        var oter_amount = sum_amount - part_amount - duty_amount;
        this.chartData2 = {
          columns: ["日期", "访问用户"],
          rows: [
            { 日期: "其他", 访问用户: oter_amount },
            { 日期: "有限合伙", 访问用户: part_amount },
            { 日期: "有限责任", 访问用户: duty_amount }
          ]
        };
      }
    },
    town_message_date: async function() {
      let params = {};
      const res = await http.post(api.town_message_date, params);
      if (res.data.value == 1) {
        this.chartData8.rows = res.data.message;
        console.log(this.chartData8.rows);
      }
    },
    company_risks: async function() {
      let params = {};
      const res = await http.post(api.company_risks, params);
      if (res.data.value == 1) {
        this.company_risk = res.data.message;
        console.log(this.company_risk);
      }
    },

    /**私募产品 */
    multi_count: async function() {
      let params = {};
      const res = await http.post(api.multi_count, params);
      var data = res.data;
      this.multiCapital_size = data.multiCapital_size;
      this.multiCompany_amount = data.multiCompany_amount;
      this.multiManager_amount = data.multiManager_amount;
      this.multiProduct_amount = data.multiProduct_amount;
      this.chartData3 = {
        columns: ["日期", "访问用户"],
        rows: [
          { 日期: "其他", 访问用户: data.multiOther_amount },
          { 日期: "有限合伙", 访问用户: data.multiPart_amount },
          { 日期: "有限责任", 访问用户: data.multiDuty_amount }
        ]
      };
    }
  },
  created() {
    this.company_message_date();
    this.town_message_date();
    this.company_risks();
    this.multi_count();
  }
};
</script>

<style scoped>
.el-row {
  margin-bottom: 20px;
}

.el-row:last-child {
  margin-bottom: 0;
}

.el-col {
  border-radius: 4px;
}
.bg-purple-dark {
  background: #99a9bf;
}
.bg-purple {
  background: #d3dce6;
}
.bg-purple-light {
  background: #e5e9f2;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}
.row-bg {
  padding: 10px 0;
  background-color: #f9fafc;
}
.ve-histogram {
  margin-top: 10px;
  z-index: 1;
}
.ve-pie {
  margin-top: 20px;
  z-index: 1;
}

.el-cascader {
  margin-left: 10px;
}
.el-card {
  width: 200px;
  display: inline-flex;
  margin: 20px;
  text-align: center;
}
.el-card h3 {
  margin-bottom: 3px;
  color: #fa6e86;
}

.el-card__body {
  width: 100%;
  padding: 0 0 20px 0 !important;
}
.font_s {
  margin-top: 20px;
  padding-top: 10px;
  font-size: 45px;
  width: 80%;
}
.el-col {
  margin-top: 20px;
}
.shensk {
  font-size: 479px;
  padding: 0;
  line-height: 0;
}
.data-empty {
  position: relative;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.7);
  color: #888;
  font-size: 14px;
}
</style>
