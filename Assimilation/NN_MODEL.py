from tensorflow.keras.layers import Input, Dense, Flatten, Conv2D, MaxPool2D, BatchNormalization, Dropout
from tensorflow.keras.models import Model

layers_schema = {
    'Input': {
        'shape': 'tuple'
    },
    'Conv2D': {
        'filters': 'int',
        'kernel_size': 'int',
        'padding': 'str',
        'activation': 'str'
    },
    'MaxPool2D': {
        'pool_size': 'tuple'
    },
    'BatchNormalization': {},
    'Flatten': {},
    'Dense': {
        'units': 'int',
        'activation': 'str'
    },
    'Dropout': {
        'rate': 'float'
    }
}
alias_for_parsing = {
    'InputLayer': 'Input',
    'MaxPooling2D': 'MaxPool2D'
}
embedded_attributes = {
    'activation': 'activation.__name__',
    'shape': 'input_shape',
    'kernel_size': 'kernel_size[0]'
}

sp_list = {'Input': ['shape']}


def special_process(info, layer_type, param_key):
    if layer_type == 'Input':
        if param_key == 'shape':
            return info[0][1:]
        else:
            return info
    else:
        return info


def build_model():
    input = Input(shape=(224, 224, 3))
    x = Conv2D(filters=16, kernel_size=3, padding='same', activation='relu')(input)
    x = MaxPool2D(pool_size=(2, 2))(x)
    x = BatchNormalization()(x)
    x = Conv2D(filters=32, kernel_size=3, padding='same', activation='relu')(x)
    x = MaxPool2D(pool_size=(2, 2))(x)
    x = BatchNormalization()(x)
    x = Conv2D(filters=64, kernel_size=3, padding='same', activation='relu')(x)
    x = MaxPool2D(pool_size=(2, 2))(x)
    x = BatchNormalization()(x)
    x = Flatten()(x)
    x = Dense(units=64, activation='relu')(x)
    x = Dropout(rate=0.2)(x)
    x = Dense(units=32, activation='relu')(x)
    x = Dropout(rate=0.2)(x)
    x = Dense(units=16, activation='relu')(x)
    x = Dense(units=8, activation='softmax')(x)
    model = Model(inputs=input, outputs=x)
    return model


def parse_model(model):
    nodes = []
    rels = []
    for layer in model.layers:
        to_node = layer.name
        print(to_node)
        raw_type = str(type(layer)).split('.')[-1].replace("'>", "")
        if raw_type in alias_for_parsing:
            raw_type = alias_for_parsing[raw_type]
        print('Layer type:', raw_type)
        schema = layers_schema[raw_type]
        node_properties = {}
        for key in schema:
            if key in embedded_attributes:
                attr = embedded_attributes[key]
            else:
                attr = key
            value = eval('layer.{}'.format(attr))
            print(key, ':', value)
            node_properties[key] = value
        nodes.append({'name': to_node, 'type': raw_type, 'params': node_properties})
        from_node = layer.input.name.split('/')[0]
        print('Relationship:', from_node, '->', to_node)
        if from_node != to_node:
            rels.append({'from': from_node, 'to': to_node})
        print()
    return nodes, rels


if __name__ == "__main__":
    model = build_model()
    nodes, rels = parse_model(model)
    print('Done')
