package com.tracholar.demo.lambok;

import com.sun.tools.javac.api.JavacTrees;
import com.sun.tools.javac.processing.JavacProcessingEnvironment;
import com.sun.tools.javac.tree.JCTree;
import com.sun.tools.javac.tree.TreeMaker;
import com.sun.tools.javac.util.Context;
import com.sun.tools.javac.util.Names;

import javax.annotation.processing.*;
import javax.lang.model.SourceVersion;
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
@SupportedAnnotationTypes("com.tracholar.demo.lambok.MyGetterSetter")
@SupportedSourceVersion(SourceVersion.RELEASE_8)
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
        messager.printMessage(Diagnostic.Kind.NOTE, "我是处理器。。。。");
        Set<? extends Element> elementsWithAnnotation = roundEnv.getElementsAnnotatedWith(MyGetterSetter.class);
        for(Element element : elementsWithAnnotation){
            messager.printMessage(Diagnostic.Kind.NOTE, element.getSimpleName());
        }

        return true;
    }

    private JCTree.JCMethodDecl makeGetter(JCTree.JCVariableDecl variableDecl){
        return null;
    }

    private JCTree.JCMethodDecl makeSetter(JCTree.JCVariableDecl variableDecl){
        return null;
    }

    private Name newGetName(Name name){
        return names.fromString("get" + name.toString().toUpperCase());
    }

    private Name newSetName(Name name){
        return names.fromString("set" + name.toString().toUpperCase());
    }
}
