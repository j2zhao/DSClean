import numpy as np
import typing
import random
import string
import os
import pickle
import inspect
import time


# time stamp + line numbers

def write_log(file, timestamp, function_name, input_ids=[], output_ids=[], frame=None, args=None):
    # if function_name == '__getitem__':  # handle edge case
    #     return

    if not frame:
        frame_info = inspect.stack()[-1]
    else:
        frame_info = inspect.getframeinfo(frame)

    if frame_info:
        fileline = ','.join([str(frame_info.filename), str(frame_info.lineno)])
        code_context = frame_info.code_context
    else:
        fileline = ''
        code_context = ''

    args = str(args)
    log = {'time': timestamp, 'filename': fileline, 'context': code_context, 'function_name': function_name, 'input_ids': input_ids,
           'output_ids': output_ids, 'args': args}
    log = str(log)
    log = log + '\n'
    file.write(log)


def write_child_log(file, time, parent_ids, child_ids):
    if isinstance(parent_ids, list):
        parent_ids = ','.join(parent_ids)
    if isinstance(child_ids, list):
        parent_ids = ','.join(child_ids)
    log = '{};relation;{};{}\n'.format(time, parent_ids, child_ids)
    file.write(log)


def write_new_log(file, time, id):
    log = '{};new;{}\n'.format(time, id)
    file.write(log)


def rand_string(N):
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(N))


class LoggedNDArray(np.ndarray):
    file_name = '/tmp/logs/log.txt'
    directory = '/tmp/logs'
    next_id = 1

    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        return obj

    def __array_finalize__(self, obj):
        # if obj is None:
        self.file = open(self.file_name, 'a+')
        if isinstance(obj, LoggedNDArray):
            id_ = str(obj.get_id())
            self.write_log = getattr(obj, 'write_log', True)
            if self.write_log:
                write_child_log(self.file, time.time(), id_, str(self.get_id()))
        else:
            self.write_log = True
            write_new_log(self.file, time.time(), str(self.get_id()))

    def __getitem__(self, key) -> typing.Any:
        if self.write_log:
            write_log(self.file, str(time.time()), self.__getitem__.__name__, input_ids=self.get_id(),
                      args={'key': key})
        return super().__getitem__(key)

    def __setitem__(self, key, value) -> None:
        if self.write_log:
            write_log(self.file, str(time.time()), self.__setitem__.__name__, input_ids=self.get_id(),
                      args={'key': key})
        self.file.write(str(self.funct) + " ; " + self.__setitem__.__name__ + " ; " + str(key) + '\n')

        return super().__setitem__(key, value)

    def get_id(self, index=None):
        if not hasattr(self, 'id'):
            self.id = LoggedNDArray.next_id
            LoggedNDArray.next_id += 1
        if index != None:
            id_ = str(self.id) + '_' + index
        else:
            id_ = self.id
        id_ = (self.shape, id_)
        return id_

    def set_write_log(self, value):
        self.write_log = value

    def take(self, indices, axis=None, out=None, mode='raise'):
        if self.write_log:
            if out != None:
                out = out.view(np.ndarray)
            output = super().take(indices, axis, out, mode)
            output = output.view(LoggedNDArray)
            output.set_write_log(self.write_log)
            args = {}
            args['indices'] = str(indices)
            args['axis'] = str(axis)
            args['mode'] = str(mode)

            if self.write_log:
                write_child_log(self.file, time.time(), str(self.get_id()), str(output.get_id()))
                write_log(self.file, str(time.time()), self.take.__name__, input_ids=self.get_id(),
                          output_ids=output.get_id(), args=args)
            return output
        else:
            return super().take(indices, axis, out, mode)

        # self.file.write(str(self.funct) + " ; " + self.take.__name__ + " ; "  + str(kwargs) + '\n')

    # def __getattr__(self, name):
    #     if self.write_log:
    #         write_log(self.file, str(time.time()), self.__getattr__.__name__, input_ids=str(self.get_id()), args = {'name': name})
    #     print(type(super()))
    #     return super().__getattr__(name)

    def __array_ufunc__(self, ufunc, method, *inputs, out=None, where=True, **kwargs):
        args = []
        input_ids = []
        # input_ids.append(str(self.get_id()))
        logged_args = {}
        new_nd_arrays = []

        for input_ in inputs:
            if isinstance(input_, LoggedNDArray):
                args.append(input_.view(np.ndarray))
                input_ids.append(input_.get_id())
            elif isinstance(input_, np.ndarray):
                args.append(input_)
                id_file = str(id(input_)) + '_' + rand_string(10)
                id_ = (input_.shape, id_file)
                new_nd_arrays.append((self.file, time.time(), id_))
                array_path = os.path.join(self.directory, id_file + '.npy')
                with open(array_path, 'w') as file:
                    np.save(file, input_)
                input_ids.append(id_)
            else:
                args.append(input_)
                input_ids.append(input_)

        # deal with ufunc methods
        if method == 'reduceat' or method == 'at':
            if isinstance(inputs[1], LoggedNDArray):
                logged_args['indices'] = inputs[1].get_id(rand_string(10))
                array_path = os.path.join(self.directory, logged_args['indices'][1] + '.npy')
                logged_args['indices'] = str(logged_args['indices'])
                input_ids[1] = logged_args['indices']
                with open(array_path, 'w') as file:
                    np.save(file, args[1])

            elif isinstance(inputs[1], np.array):
                logged_args['indices'] = input_ids[1]
            # if indices is a tuple

            elif isinstance(inputs[1], tuple):
                indices = []
                args[1] = []
                for index in inputs[1]:
                    if isinstance(index, LoggedNDArray):
                        id_ = index.get_id(rand_string(10))
                        indices.append(str(id_))
                        array_path = os.path.join(self.directory, id_[1] + '.npy')
                        arr = index.view(np.ndarray)
                        args[1].append(arr)
                        with open(array_path, 'w') as file:
                            np.save(file, arr)

                    elif isinstance(index, np.array):
                        id_file = str(id(index)) + '_' + rand_string(10)
                        id_ = str((index.shape, id_file))
                        indices.append(id_)
                        array_path = os.path.join(self.directory, id_file + '.npy')
                        args[1].append(index)
                        with open(array_path, 'w') as file:
                            np.save(file, index)

                    else:
                        id_file = str(id(index)) + '_' + rand_string(10)
                        indices.append(str(('object', id_file)))
                        obj_path = os.path.join(self.directory, id_file + '.pickle')
                        with open(obj_path, 'w') as file:
                            np.save(file, index)

                args[1] = tuple(args[1])
                logged_args['indices'] = str(indices)
            else:
                id_file = str(id(inputs[1])) + '_' + rand_string(10)
                logged_args['indices'] = str(('object', id_file))
                obj_path = os.path.join(self.directory, id_file + '.pickle')
                with open(obj_path, 'w') as file:
                    pickle.dump(inputs[1], file)

        # deal with out argument
        if isinstance(out, LoggedNDArray):
            outputs = out.view(np.ndarray)
        elif isinstance(out, list):
            outputs = []
            for out_ in out:
                if isinstance(out_, LoggedNDArray):
                    outputs.append(out_.view(np.ndarray))
        else:
            outputs = out

        if not isinstance(outputs, list):
            kwargs['out'] = outputs
        else:
            if outputs != None:
                kwargs['out'] = tuple(outputs)

        # deal with where argument
        if isinstance(where, LoggedNDArray):
            w = where.view(np.ndarray)
            id_ = where.get_id(rand_string(10))
            array_path = os.path.join(self.directory, id_[1] + '.npy')
            with open(array_path, 'w') as file:
                np.save(file, w)
            logged_args['where'] = str(id_)

        elif isinstance(where, np.ndarray):
            w = where
            id_ = str(id(where)) + '_' + rand_string(10)
            logged_args['where'] = str((where.shape, id_))
            array_path = os.path.join(self.directory, str(id_) + '.npy')
            with open(array_path, 'w') as file:
                np.save(file, w)

        elif where is not True:
            w = where
            id_file = str(id(where)) + '_' + rand_string(10)
            logged_args['where'] = str(('object', id_file))
            obj_path = os.path.join(self.directory, id_file + '.pickle')
            with open(obj_path, 'w') as file:
                pickle.dump(where, file)
        else:
            w = True

        if w is not True:
            kwargs['where'] = w

        results = super().__array_ufunc__(ufunc, method,
                                          *args, **kwargs)

        if results is NotImplemented:
            return NotImplemented

        if ufunc.nout == 1:
            results = (results,)

        results_ = []
        output_ids = []
        if outputs == None:
            for result in results:
                if isinstance(result, LoggedNDArray):
                    results_.append(result)
                    output_ids.append(result.get_id())

                elif isinstance(result, np.ndarray):
                    result_ = result.view(LoggedNDArray)
                    results_.append(result_)
                    output_ids.append(result_.get_id())
                elif result is None:
                    pass
                else:
                    results_.append(result)
                    output_ids.append(result)
        else:
            if not isinstance(outputs, tuple):
                outputs = (outputs,)
            for result, output in zip(results, outputs):
                if output == None:
                    if isinstance(result, np.ndarray):
                        results_.append(result.view(LoggedNDArray))
                    else:
                        results_.append(result)
                else:
                    results_.append(output)
                    output_ids.append(None)

        results = tuple(results_)
        # write array without output, where, and methods
        name = ufunc.__name__ + ',' + method
        # these are already saved by their ids in logged_args or output_id
        if 'out' in kwargs:
            del kwargs['out']
        if 'where' in kwargs:
            del kwargs['where']
        args = kwargs.update(logged_args)
        if self.write_log:
            write_log(self.file, str(time.time()), name, input_ids=input_ids, output_ids=output_ids, args=args)

        if method == 'at':
            return
        return results[0] if len(results) == 1 else results
