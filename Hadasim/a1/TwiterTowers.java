
import javafx.application.Platform;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.event.ActionEvent;
import javafx.scene.control.ComboBox;
import javafx.scene.control.Label;
import javafx.scene.shape.Line;
import javafx.scene.shape.Polyline;
import javafx.scene.shape.Rectangle;

public class TwiterTowers {

    @FXML
    private ComboBox<String> comboBox;

    @FXML
    private Label rHLabel;

    @FXML
    private Line rHight;

    @FXML
    private Rectangle rectangle;

    @FXML
    private Label tHLabel;

    @FXML
    private Line tHight;

    @FXML
    private TextField widthTxt;

    @FXML
    private TextField hightTxt;

    @FXML
    private Label towerHight;

    @FXML
    private Label towerWidth;

    @FXML
    private Polyline triangle;

    @FXML
    private Label wLabel;
    @FXML
    private Label optionLabel;

    @FXML
    private Line width;

    @FXML
    private Button applySizeButton;

    private int userWidth, userHight;

    private boolean isRect, isTri;

    private ObservableList<String> options=  FXCollections.observableArrayList("Rectangle", "Triangle", "Exit","");

    public void initialize() {
        comboBox.getItems().addAll(options);//adds the options to ComboBox
        isRect = false;
        isTri = false;
    }
    @FXML
    void selectedOption(ActionEvent event) {
        String option = comboBox.getValue();
        comboBox.setVisible(false);
        optionLabel.setVisible(false);
        switch (option){
            case "Rectangle":
                rectangle.setVisible(true);
                rHLabel.setVisible(true);
                rHight.setVisible(true);
                setVis();
                isRect= true;
                break;
            case "Triangle":
                triangle.setVisible(true);
                tHLabel.setVisible(true);
                tHight.setVisible(true);
                setVis();
                isTri = true;
                break;
            case "Exit":
                Platform.exit();
                System.exit(0);
                break;
        }

    }

    private void handelTri() {
        if (userWidth % 2 == 0 || userWidth > (userHight * 2))
        {
            System.out.println("Its imposable to print triangle");
            restart();
            return;
        }
        String stars = "";
        int jump = 0;
        if(userWidth==3)//to avoid a division by zero
        {
            for (int i = 0; i < userHight - 1; i++)
                System.out.println(" *");
            System.out.println("***");
        }
        else {
            int numFirstGroup = 0;
            int numGroups = (userWidth / 2) + 1;
            int numPerGroup = (userHight - 2) / (numGroups - 2);
            if (((userHight - 2) % (numGroups - 2)) != 0)
                numFirstGroup = ((userHight - 2) % (numGroups - 2));
            for (int i = 0; i < numGroups; i++) {
                for (int j = 0; j < (userWidth - 1 - jump) / 2; j++) {
                    stars += " ";
                }
                for (int j = 0; j < jump + 1; j++) {
                    stars += "*";
                }
                for (int j = 0; j < (userWidth - 1 - jump) / 2; j++) {
                    stars += " ";
                }
                if (i == 0 || i == numGroups - 1)
                    System.out.println(stars);
                else {
                    if (i == 1)
                        for (int j = 0; j < numPerGroup + numFirstGroup; j++) {
                            System.out.println(stars);
                        }
                    else
                        for (int j = 0; j < numPerGroup; j++) {
                            System.out.println(stars);
                        }
                }
                stars = "";
                jump += 2;
            }
        }
        restart();
    }

    private void handelRect() {
        if(Math.abs(userWidth-userHight)>5)
            System.out.println("Rectangle's area is: " + userWidth*userHight);
        else
            System.out.println("Rectangle's scope is: " + (userWidth*2 + userHight*2));
        restart();
    }

    @FXML
    void getSize(ActionEvent event) {
        userWidth = Integer.parseInt(widthTxt.getText());
        userHight = Integer.parseInt(hightTxt.getText());
        if(isRect)
            handelRect();
        else
            handelTri();
    }

    private void setVis() {
        width.setVisible(true);
        wLabel.setVisible(true);
        towerHight.setVisible(true);
        towerWidth.setVisible(true);
        hightTxt.setVisible(true);
        widthTxt.setVisible(true);
        applySizeButton.setVisible(true);
    }

    private void restart() {
        widthTxt.setText("");
        hightTxt.setText("");
        comboBox.getSelectionModel().selectLast();
        optionLabel.setVisible(true);
        comboBox.setVisible(true);
        width.setVisible(false);
        wLabel.setVisible(false);
        towerHight.setVisible(false);
        towerWidth.setVisible(false);
        hightTxt.setVisible(false);
        widthTxt.setVisible(false);
        applySizeButton.setVisible(false);
        triangle.setVisible(false);
        tHLabel.setVisible(false);
        tHight.setVisible(false);
        rectangle.setVisible(false);
        rHLabel.setVisible(false);
        rHight.setVisible(false);
        isRect = false;
        isTri = false;
    }
}
