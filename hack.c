#define PY_SSIZE_T_CLEAN
#include <python3.8/Python.h>

static PyObject *foo(PyObject *self, PyObject *args)
{
    // printf("foo");
    fflush(stdout);
    PyObject *float_list;
    int pr_length;
    double *pr;

    if (!PyArg_ParseTuple(args, "O", &float_list))
    {
        printf("not parsed");
        fflush(stdout);
        return NULL;
    }
    // printf("parsed");
    // fflush(stdout);

    pr_length = PyObject_Length(float_list);
    if (pr_length < 0)
        return NULL;

    pr = (double *)malloc(sizeof(double *) * pr_length);

    if (pr == NULL)
        return NULL;

    for (int index = 0; index < pr_length; index++)
    {
        PyObject *item;
        item = PyList_GetItem(float_list, index);
        if (!PyFloat_Check(item))
            pr[index] = 0.0;
        pr[index] = PyFloat_AsDouble(item);
    }

    PyObject *result = PyList_New(0);

    for (int index = 0; index < pr_length; index++)
    {
        PyList_Append(result, PyLong_FromLong(pr[index] * 5));
    }
    free(pr);

    return result;
}

static PyMethodDef FooMethods[] =
    {
        {"foo", foo, METH_VARARGS, "..."},
        {NULL, NULL, 0, NULL}};

static struct PyModuleDef fooMod =
    {
        PyModuleDef_HEAD_INIT,
        "foo", /* name of module */
        "",    /* module documentation, may be NULL */
        -1,    /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
        FooMethods};

PyMODINIT_FUNC PyInit_fooMod(void)
{
    return PyModule_Create(&fooMod);
}

using namespace motion_planning::collision_checker;
// update drivable area with objects

cv::Mat drivable_area_with_objects = [&]()
{
    nami::Grid grid_map(*occupancy_grid_);
    autoware_perception_msgs::msg::DynamicObjectArray static_objects;
    for (const auto &obj : object_ptr_->objects)
    {
        if (
            /*obj.shape.type == autoware_perception_msgs::msg::Shape::BOUNDING_BOX &&*/
            obj.state.twist_covariance.twist.linear.x < 1.0)
        {
            static_objects.objects.push_back(obj);
        }
    }
    grid_map.addObjects(static_objects.objects, 0.5, 0.2);
    cv::Mat drivable_area = transposeCVData(grid_map.data());
    drivable_area.forEach<unsigned char>(
        [&](unsigned char &value, const int *position) -> void
        { value = (value > 0) ? 0 : 255; });
    return drivable_area;
}();
cv::Mat clearance_map_with_objects = getClearanceMap(drivable_area_with_objects);
auto map_with_obst_ptr =
    std::make_unique<Map>(*occupancy_grid_, drivable_area_with_objects, clearance_map_with_objects);
auto cc_map_with_obst_ptr = std::make_unique<GridMapCollisionChecker>(*map_with_obst_ptr, ego_params_);
for (const auto &state : reference_states)
{
    motion_planning::collision_checker::State state_cc = {state.x, state.y, state.z};
    if (!cc_map_with_obst_ptr->isSingleStateCollisionFreeImproved(state_cc))
    {
        RCLCPP_ERROR(get_logger(), "GRID MAP COLLISION");
        break;
    }
}
