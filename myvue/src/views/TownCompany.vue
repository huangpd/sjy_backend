<template>
  <el-row id="TownCompany">
    <el-col :span="5">
      <el-form ref="form" :model="ruleForm" label-width="80px">
        <el-form-item label="公司名字">
          <el-input v-model="ruleForm.company_name" style="width: 260px"></el-input>
        </el-form-item>

        <el-form-item label="统一代码">
          <el-input v-model="ruleForm.company_uid" style="width: 260px"></el-input>
        </el-form-item>

        <el-form-item label="小镇选择">
          <el-select v-model="ruleForm.company_town_uid" placeholder="请选择区域">
            <el-option :label="i.name" :value="i.uid" v-for="i in town" :key="i.id"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="联系人">
          <el-input v-model="ruleForm.username" style="width: 260px"></el-input>
        </el-form-item>

        <el-form-item label="联系电话">
          <el-input v-model="ruleForm.phone" style="width: 260px"></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm(ruleForm)">立即创建</el-button>
          <el-button @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
      </el-form>

      <el-upload class="upload-demo" drag action="../xls/" multiple :on-success="upload_success">
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">
          将文件拖到此处，或
          <em>点击上传</em>
        </div>
        <div class="el-upload__tip" slot="tip">只能上传.xls文件!</div>
      </el-upload>
    </el-col>

    <el-col :span="15">
      <div style="margin-bottom: 20px;">
        <span>地区筛选:</span>
        <el-button-group>
          <el-cascader size="large" :options="options" @change="handleChange"></el-cascader>
        </el-button-group>
        <el-button type="primary" @click="export_excel(1)">导出到Excel文件</el-button>
      </div>

      <el-card class="box-card" style="width: 100%">
        <el-table :data="tableData" style="width: 100%">
          <el-table-column prop="company_name" label="公司名字"></el-table-column>
          <el-table-column prop="company_uid" label="统一代码"></el-table-column>
          <el-table-column prop="company_town_name" label="入驻小镇"></el-table-column>
          <el-table-column prop="username" label="联系人"></el-table-column>
          <el-table-column prop="phone" label="联系电话"></el-table-column>

          <el-table-column fixed="right" label="操作" width="150">
            <template slot-scope="scope">
              <el-button
                index="/Company_Details/"
                @click.native.prevent="company_amend_details(scope.$index ,scope.row)"
                type="text"
                size="small"
              >查看详情</el-button>
              <el-button
                @click.native.prevent="company_amend_open(scope.$index ,scope.row)"
                type="text"
                size="small"
              >修改</el-button>
              <el-button
                @click.native.prevent="company_delete(scope.$index ,scope.row)"
                type="text"
                size="small"
              >移除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-col>

    <el-dialog title="公司信息修改" :visible.sync="dialogFormVisible">
      <el-form :model="company_amend_form" label-width="80px">
        <el-form-item label="公司名字">
          <el-input v-model="company_amend_form.company_name" style="width: 260px"></el-input>
        </el-form-item>

        <el-form-item label="统一代码">
          <el-input v-model="company_amend_form.company_uid" style="width: 260px"></el-input>
        </el-form-item>

        <el-form-item label="小镇选择">
          <el-select v-model="company_amend_form.company_town_uid" placeholder="请选择区域">
            <el-option :label="i.name" :value="i.uid" v-for="i in town" :key="i.id"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="联系人">
          <el-input v-model="company_amend_form.username" style="width: 260px"></el-input>
        </el-form-item>

        <el-form-item label="联系电话">
          <el-input v-model="company_amend_form.phone" style="width: 260px"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="company_amend()">确 定</el-button>
      </div>
    </el-dialog>
  </el-row>
</template>

<script>
import http from "@/utils/http";
import api from "@/utils/api";
import jsonToExcel from "@/utils/jsonToExcel";
import Bus from "@/assets/bus.js";
import { regionDataPlus, CodeToText } from "element-china-area-data";

export default {
  name: "TownCompany",
  data() {
    return {
      province: "",
      city: "",
      area: "",
      is_export: "",
      company_amend_form: {
        uid: "",
        company_name: "",
        company_uid: "",
        company_town_uid: "",
        company_town_name: "",
        username: "",
        phone: ""
      },
      area: [],
      dialogFormVisible: false,
      options: [
        {
          value: "全部",
          label: "全部"
        }
      ],

      // selectedOptions: [],
      ruleForm: {
        company_name: "",
        company_uid: "",
        company_town_uid: "",
        company_town_name: "",
        username: "",
        phone: ""
      },
      tableData: [],
      town: []
    };
  },
  methods: {
    /**按地区筛选公司 */
    handleChange(value) {
      var is_export = 0;
      value[0] ? (this.province = value[0]) : (this.province = "全部");
      value[1] ? (this.city = value[1]) : (this.city = "全部");
      value[2] ? (this.area = value[2]) : (this.area = "全部");
      this.company_message_v(this.province, this.city, this.area, is_export);
    },

    update(e) {},

    /**公司数据加载 */
    company_message_v: async function(province, city, area, is_export) {
      var data;
      let params = {
        is_export: is_export,
        province: province,
        city: city,
        area: area
      };
      const res = await http.post(api.company_message_v, params);
      if (res.data) {
        this.tableData = res.data;
        data = res.data;
      }
    },

    /**导出excel表格 */
    export_excel: async function(is_export) {
      let params = {
        is_export: is_export,
        province: this.province,
        city: this.city,
        area: this.area
      };
      const res = await http.post(api.company_message_v, params);
      var filename = res.data;
      let link = document.createElement("a"); //通过创建a标签实现
      link.href = "/company_message_export/";
      link.href += filename; //对下载的文件命名
      link.download = "导出的文件";
      document.body.appendChild(link);

      link.click();
      document.body.removeChild(link);
    },

    /**表单提交 */
    submitForm: async function() {
      this.ruleForm.company_town_name = this.town.filter(
        t => t.uid == this.ruleForm.company_town_uid
      )[0].name;
      let params = this.ruleForm;
      const res = await http.post(api.company_add, params);
      if (res.data.value == 1) {
        var y = this.tableData;
        y.push(res.data.message);
      } else {
        this.$message({
          message: res.data.message,
          type: "warning"
        });
      }
    },

    /**清空表单 */
    resetForm() {
      this.ruleForm.resetFields();
    },

    /**加载小镇 */
    town_message: async function() {
      let params = [];
      const res = await http.post(api.town_message, params);
      if (res.data) {
        this.town = res.data;
        // console.log(this.town);
      }

      for (var i = 0; i < res.data.length; i++) {
        var area = "";
        area +=
          res.data[i].province +
          "-" +
          res.data[i].city +
          "-" +
          res.data[i].area +
          "-" +
          res.data[i].name;
        this.area.push(area);
      }
      this.area = Array.from(new Set(this.area));
      var is_breakPro = false;
      var is_breakCity = false;
      // console.log(this.area);
      for (var i = 0; i < this.area.length; i++) {
        is_breakPro = false;
        is_breakCity = false;

        for (var j = 0; j < this.options.length; j++) {
          if (is_breakPro) {
            break;
          }
          if (this.area[i].substring(0, 3) == this.options[j].value) {
            for (var o = 0; o < this.options[j].children.length; o++) {
              if (is_breakCity) {
                break;
              }
              if (
                this.area[i].substring(4, 7) ==
                this.options[j].children[o].value
              ) {
                for (
                  var p = 0;
                  p < this.options[j].children[o].children.length;
                  p++
                ) {
                  if (
                    this.area[i].substring(8, 11) ==
                    this.options[j].children[o].children[p].value
                  ) {
                    is_breakCity = true;
                    is_breakPro = true;
                    break;
                  } else if (
                    p >=
                    this.options[j].children[o].children.length - 1
                  ) {
                    this.options[j].children[o].children.push({
                      value: this.area[i].substring(8, 11),
                      label: this.area[i].substring(8, 11)
                    });
                    // console.log("插入了", this.area[i].substring(8, 11));
                    is_breakCity = true;
                    is_breakPro = true;
                    break;
                  }
                }
              } else if (o >= this.options[j].children.length - 1) {
                this.options[j].children.push({
                  value: this.area[i].substring(4, 7),
                  label: this.area[i].substring(4, 7),
                  children: [
                    {
                      value: "全部",
                      label: "全部"
                    }
                  ]
                });
                this.options[j].children[o + 1].children.push({
                  value: this.area[i].substring(8, 11),
                  label: this.area[i].substring(8, 11)
                });
                // console.log("插入了", this.area[i].substring(4, 11));
                is_breakPro = true;
                break;
              }
            }
          } else if (j >= this.options.length - 1) {
            this.options.push({
              value: this.area[i].substring(0, 3),
              label: this.area[i].substring(0, 3),
              children: [
                {
                  value: "全部",
                  label: "全部"
                }
              ]
            });
            this.options[j + 1].children.push({
              value: this.area[i].substring(4, 7),
              label: this.area[i].substring(4, 7),
              children: [
                {
                  value: "全部",
                  label: "全部"
                }
              ]
            });
            this.options[j + 1].children[1].children.push({
              value: this.area[i].substring(8, 11),
              label: this.area[i].substring(8, 11)
            });
            // console.log("插入了", this.area[i]);
            break;
          }
        }
      }
    },

    /**加载公司 */
    company_message: async function() {
      let params = [];
      const res = await http.post(api.company_message, params);
      if (res.data) {
        // console.log(res.data);
        this.tableData = res.data;
      }
    },

    /**删除公司 */
    company_delete: async function(index, row) {
      var date = { uid: row.uid };
      let params = date;
      const res = await http.post(api.company_delete, params);
      if (res.data) {
        let data = res.data;
        if (data.value == 1) {
          this.tableData.splice(index, 1);
        } else {
          this.$message({
            message: data.message,
            type: "warning"
          });
        }
      }
    },

    /**修改公司对话框弹出 */
    company_amend_open(index, row) {
      this.dialogFormVisible = true;
      this.company_amend_form = row;
    },

    /**公司详情 */
    company_amend_details(index, row) {
      this.$router.push({
        name: "Company_Details",
        params: {
          id: row.id
        }
      });
    },

    /**修改公司提交 */
    company_amend: async function() {
      this.company_amend_form.company_town_name = this.town.filter(
        t => t.uid == this.company_amend_form.company_town_uid
      )[0].name;
      let params = this.company_amend_form;
      const res = await http.post(api.company_amend, params);
      if (res.data) {
        let data = res.data;
        if (data.value == 1) {
          this.$message({
            message: data.message,
            type: "warning"
          });
        } else {
          this.$message({
            message: data.message,
            type: "warning"
          });
        }
        this.dialogFormVisible = false;
      }
    },

    /**加载成功 */
    upload_success(response, file, fileList) {
      if (response.value == 1) {
        this.company_message();
      } else {
        this.$message({
          message: response.message,
          type: "warning"
        });
      }
    }
  },

  /**页面加载 */
  created() {
    this.town_message();
    // this.company_message();
  }
};
</script>

<style>
.el-cascader {
  margin-left: 0;
  width: 260px;
}
.el-upload {
  z-index: 2;
}
</style>
