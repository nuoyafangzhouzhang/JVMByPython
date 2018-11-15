from ch08.rtda.Thread import Thread

class Interpreter():

    @staticmethod
    def interpret(method, logInst, args):
        thread = Thread()
        frame = thread.newFrame(method)
        thread.pushFrame(frame)

        jArgs = Interpreter.createArgsArray(method.getClass().loader, args)
        frame.localVars.setRef(0, jArgs)

        try:
            Interpreter.loop(thread, logInst)
        except RuntimeError as e:
            Interpreter.logFrames(thread)
            print("LocalVars: {0}".format(frame.localVars))
            print("OperandStack: {0}".format(frame.operandStack))
            print(e)


    @staticmethod
    def loop(thread, logInst):
        from ch08.instructions.base.BytecodeReader import BytecodeReader
        from ch08.instructions.Factory import Factory

        reader = BytecodeReader()

        while True:
            frame = thread.currentFrame()
            pc = frame.nextPC
            thread.pc = pc

            reader.reset(frame.method.code, pc)
            opcode = reader.readUint8()
            inst = Factory.newInstruction(opcode)
            inst.fetchOperands(reader)
            frame.nextPC = reader.pc

            if logInst:
                Interpreter.logInstruction(frame, inst)

            inst.execute(frame)
            if thread.isStackEmpty():
                break

    @staticmethod
    def logFrames(thread):
        while not thread.isStackEmpty():
            frame = thread.popFrame()
            method = frame.method
            className = method.getClass().name
            print(">> pc: {0:4} {1}.{2}{3}".format(frame.nextPC, className, method.name, method.descriptor))

    @staticmethod
    def logInstruction(frame, inst):
        method = frame.method
        className = method.getClass().name
        methodName = method.name
        pc = frame.thread.pc
        print("{0}.{1} #{2:<2} {3} {4}".format(className, methodName, pc, inst.__class__.__name__, Interpreter.prn_obj(inst)))

    @staticmethod
    def createArgsArray(loader, args):
        from ch08.rtda.heap.StringPool import StringPool

        stringClass = loader.loadClass("java/lang/String")
        argsArr = stringClass.arrayClass().newArray(len(args))
        jArgs = argsArr.refs
        for i, arg in args:
            jArgs[i] = StringPool.JString(loader, arg)
        return argsArr

    @staticmethod
    def prn_obj(obj):
        return ' '.join(['%s:%s' % item for item in obj.__dict__.items()])