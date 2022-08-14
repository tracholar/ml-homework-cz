package com.tracholar.demo.lambok;

import com.sun.source.tree.Tree;
import com.sun.tools.javac.api.JavacTrees;
import com.sun.tools.javac.code.Flags;
import com.sun.tools.javac.code.Type;
import com.sun.tools.javac.processing.JavacProcessingEnvironment;
import com.sun.tools.javac.tree.JCTree;
import com.sun.tools.javac.tree.TreeMaker;
import com.sun.tools.javac.tree.TreeTranslator;
import com.sun.tools.javac.util.Context;
import com.sun.tools.javac.util.Names;

import javax.annotation.processing.AbstractProcessor;
import javax.annotation.processing.Messager;
import javax.annotation.processing.ProcessingEnvironment;
import javax.annotation.processing.RoundEnvironment;
import javax.lang.model.element.Element;
import javax.lang.model.element.Name;
import javax.lang.model.element.TypeElement;
import javax.tools.Diagnostic;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;

/**
 * @author zuoyuan
 * @date 2022/8/11 10:35
 */
public class MyGetterSetterProcessor extends AbstractProcessor {
    private Messager messager;
    private JavacTrees javacTrees;
    private TreeMaker treeMaker;
    private Names names;

    @Override
    public synchronized void init(ProcessingEnvironment processingEnv) {
        super.init(processingEnv);

        messager = processingEnv.getMessager();
        javacTrees = JavacTrees.instance(processingEnv);
        Context context = ((JavacProcessingEnvironment)processingEnv).getContext();
        treeMaker = TreeMaker.instance(context);
        names = Names.instance(context);

    }

    @Override
    public boolean process(Set<? extends TypeElement> annotations, RoundEnvironment roundEnv) {
        Set<? extends Element> elementsWithAnnotation = roundEnv.getElementsAnnotatedWith(MyGetterSetter.class);
        for(Element element : elementsWithAnnotation){
            JCTree tree = javacTrees.getTree(element);

            tree.accept(new TreeTranslator(){
                @Override
                public void visitClassDef(JCTree.JCClassDecl classDecl) {
                    List<JCTree.JCVariableDecl>  variables = new LinkedList<>();

                    // 找到所有变量对应的JCTree
                    for(JCTree jcTree : classDecl.defs){
                        if(jcTree.getKind().equals(Tree.Kind.VARIABLE)){
                            variables.add((JCTree.JCVariableDecl) jcTree);
                        }
                    }

                    // 添加get/set方法
                    for(JCTree.JCVariableDecl variableDecl : variables){
                        messager.printMessage(Diagnostic.Kind.NOTE, variableDecl.getName() + " has been processed.");

                        classDecl.defs = classDecl.defs.prepend(makeGetter(variableDecl));
                        classDecl.defs = classDecl.defs.prepend(makeSetter(variableDecl));
                    }
                }
            });
        }

        JCTree.JCExpression methodType = treeMaker.Type(new Type.JCVoidType());



        return treeMaker.MethodDef(treeMaker.Modifiers(Flags.Flag.PUBLIC),
                newSetName());
    }

    private JCTree.JCMethodDecl makeGetter(JCTree.JCVariableDecl variableDecl){

    }

    private JCTree.JCMethodDecl makeSetter(JCTree.JCVariableDecl variableDecl){

    }

    private Name newGetName(Name name){
        return names.fromString("get" + name.toString().toUpperCase());
    }

    private Name newSetName(Name name){
        return names.fromString("set" + name.toString().toUpperCase());
    }
}
