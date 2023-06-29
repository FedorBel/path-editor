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
